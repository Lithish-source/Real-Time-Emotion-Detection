"""
Real-Time Emotion Detection API
Analyzes text and detects emotions using NLP
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
from collections import Counter
import math

app = Flask(__name__)
CORS(app)

# Emotion keywords dictionary
EMOTION_KEYWORDS = {
    'joy': ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'great', 'excellent', 
            'fantastic', 'love', 'beautiful', 'awesome', 'thrilled', 'delighted', 'cheerful',
            'glad', 'pleased', 'joyful', 'ecstatic', 'blissful'],
    'sadness': ['sad', 'unhappy', 'depressed', 'miserable', 'heartbroken', 'disappointed',
                'unfortunate', 'terrible', 'awful', 'crying', 'tears', 'sorrow', 'gloomy',
                'melancholy', 'upset', 'hurt', 'pain', 'lonely'],
    'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'irritated', 
              'outraged', 'hate', 'disgusted', 'enraged', 'livid', 'hostile', 'bitter',
              'rage', 'aggressive', 'violent'],
    'fear': ['scared', 'afraid', 'frightened', 'terrified', 'anxious', 'worried',
             'nervous', 'panic', 'fearful', 'alarmed', 'threatened', 'dread', 'horror',
             'paranoid', 'insecure', 'helpless'],
    'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 
                 'unexpected', 'wow', 'omg', 'incredible', 'unbelievable', 'startled'],
    'love': ['love', 'adore', 'cherish', 'treasure', 'romance', 'affection', 'caring',
             'devoted', 'passionate', 'tender', 'sweetheart', 'darling'],
    'neutral': ['okay', 'fine', 'normal', 'average', 'moderate', 'standard', 'alright']
}

# Intensity modifiers
INTENSIFIERS = ['very', 'extremely', 'incredibly', 'absolutely', 'completely', 'totally', 
                'utterly', 'really', 'truly', 'deeply', 'highly', 'super']
DIMINISHERS = ['slightly', 'somewhat', 'kind of', 'sort of', 'a bit', 'barely', 
               'hardly', 'little', 'moderately', 'fairly']

# Emoji mappings
EMOTION_EMOJIS = {
    'joy': '😊',
    'sadness': '😢',
    'anger': '😠',
    'fear': '😨',
    'surprise': '😲',
    'love': '❤️',
    'neutral': '😐'
}

class EmotionAnalyzer:
    """Advanced emotion detection from text"""
    
    def __init__(self, text):
        self.text = text.lower()
        self.words = re.findall(r'\b\w+\b', self.text)
        
    def detect_emotions(self):
        """Detect primary and secondary emotions"""
        emotion_scores = {emotion: 0 for emotion in EMOTION_KEYWORDS.keys()}
        
        for i, word in enumerate(self.words):
            for emotion, keywords in EMOTION_KEYWORDS.items():
                if word in keywords:
                    base_score = 1.0
                    
                    # Check for intensifiers before the word
                    if i > 0 and self.words[i-1] in INTENSIFIERS:
                        base_score *= 1.5
                    
                    # Check for diminishers before the word
                    if i > 0 and self.words[i-1] in DIMINISHERS:
                        base_score *= 0.5
                    
                    # Check for negation
                    if i > 0 and self.words[i-1] in ['not', 'no', 'never', "don't", "doesn't", "won't"]:
                        base_score *= -0.5
                    
                    emotion_scores[emotion] += base_score
        
        # Normalize scores
        total = sum(abs(v) for v in emotion_scores.values())
        if total > 0:
            emotion_scores = {k: round((abs(v)/total)*100, 2) for k, v in emotion_scores.items()}
        
        return emotion_scores
    
    def get_sentiment_polarity(self):
        """Calculate overall sentiment (-1 to 1)"""
        positive_emotions = ['joy', 'surprise', 'love']
        negative_emotions = ['sadness', 'anger', 'fear']
        
        emotions = self.detect_emotions()
        
        positive_score = sum(emotions.get(e, 0) for e in positive_emotions)
        negative_score = sum(emotions.get(e, 0) for e in negative_emotions)
        
        if positive_score + negative_score == 0:
            return 0.0
        
        polarity = (positive_score - negative_score) / (positive_score + negative_score)
        return round(polarity, 3)
    
    def analyze_text_metrics(self):
        """Analyze text characteristics"""
        return {
            "word_count": len(self.words),
            "character_count": len(self.text),
            "exclamation_marks": self.text.count('!'),
            "question_marks": self.text.count('?'),
            "uppercase_ratio": round(sum(1 for c in self.text if c.isupper()) / max(len(self.text), 1), 3),
            "average_word_length": round(sum(len(w) for w in self.words) / max(len(self.words), 1), 2)
        }
    
    def get_dominant_emotion(self):
        """Get the strongest detected emotion"""
        emotions = self.detect_emotions()
        if not emotions or max(emotions.values()) == 0:
            return "neutral"
        return max(emotions, key=emotions.get)
    
    def emotion_confidence(self):
        """Calculate confidence level of detection"""
        emotions = self.detect_emotions()
        max_score = max(emotions.values()) if emotions else 0
        
        if max_score >= 40:
            return "high"
        elif max_score >= 20:
            return "medium"
        else:
            return "low"

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Main endpoint for emotion analysis"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    if len(text) > 5000:
        return jsonify({"error": "Text too long (max 5000 characters)"}), 400
    
    analyzer = EmotionAnalyzer(text)
    
    emotions = analyzer.detect_emotions()
    dominant = analyzer.get_dominant_emotion()
    polarity = analyzer.get_sentiment_polarity()
    metrics = analyzer.analyze_text_metrics()
    confidence = analyzer.emotion_confidence()
    
    # Determine overall sentiment
    if polarity > 0.3:
        sentiment = "positive"
        sentiment_emoji = "😊"
    elif polarity < -0.3:
        sentiment = "negative"
        sentiment_emoji = "😢"
    else:
        sentiment = "neutral"
        sentiment_emoji = "😐"
    
    return jsonify({
        "text": text,
        "dominant_emotion": dominant,
        "dominant_emoji": EMOTION_EMOJIS.get(dominant, "😐"),
        "all_emotions": emotions,
        "sentiment": sentiment,
        "sentiment_score": polarity,
        "confidence": confidence,
        "emoji": sentiment_emoji,
        "metrics": metrics,
        "summary": f"Detected {dominant} emotion with {confidence} confidence"
    })

@app.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple texts at once"""
    data = request.json
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({"error": "No texts provided"}), 400
    
    if len(texts) > 100:
        return jsonify({"error": "Too many texts (max 100)"}), 400
    
    results = []
    for text in texts:
        if text:
            analyzer = EmotionAnalyzer(text)
            results.append({
                "text": text[:100] + "..." if len(text) > 100 else text,
                "dominant_emotion": analyzer.get_dominant_emotion(),
                "sentiment_score": analyzer.get_sentiment_polarity(),
                "emoji": EMOTION_EMOJIS.get(analyzer.get_dominant_emotion(), "😐")
            })
    
    return jsonify({"results": results, "count": len(results)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy", 
        "service": "Emotion Detector API",
        "version": "1.0.0",
        "supported_emotions": list(EMOTION_KEYWORDS.keys())
    })

if __name__ == '__main__':
    print("=" * 60)
    print("😊 Real-Time Emotion Detection API Starting...")
    print("=" * 60)
    print("🎭 Supported Emotions: Joy, Sadness, Anger, Fear, Surprise, Love")
    print("📍 Access at: http://127.0.0.1:5001/")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5001, debug=True)