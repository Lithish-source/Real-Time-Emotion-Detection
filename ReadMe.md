# 🎭 Real-Time Emotion Detector

A powerful web application that analyzes text and detects emotions using Natural Language Processing (NLP). Built with Flask and vanilla JavaScript.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **Real-Time Emotion Detection**: Analyzes text and identifies 7 different emotions (Joy, Sadness, Anger, Fear, Surprise, Love, Neutral)
- **Sentiment Analysis**: Calculates overall sentiment polarity (-1 to 1)
- **Confidence Scoring**: Provides confidence levels for emotion detection
- **Text Metrics**: Analyzes word count, character count, punctuation usage, and more
- **Intensity Detection**: Recognizes emotional intensifiers and diminishers
- **Batch Processing**: Analyze multiple texts at once via API
- **Beautiful UI**: Modern, responsive interface with animations and emoji support
- **RESTful API**: Easy-to-use API endpoints for integration

## 🚀 Demo

![Emotion Detector Demo](demo.gif)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/emotion-detector.git
cd emotion-detector
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Running the Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Open your browser and navigate to**
```
http://127.0.0.1:5001/
```

3. **Enter text and click "Analyze Emotion"** to see the results!

### API Endpoints

#### 1. Analyze Single Text
```bash
POST /analyze
Content-Type: application/json

{
  "text": "I'm so happy and excited about this amazing opportunity!"
}
```

**Response:**
```json
{
  "text": "I'm so happy and excited about this amazing opportunity!",
  "dominant_emotion": "joy",
  "dominant_emoji": "😊",
  "all_emotions": {
    "joy": 75.5,
    "sadness": 0,
    "anger": 0,
    "fear": 0,
    "surprise": 24.5,
    "love": 0,
    "neutral": 0
  },
  "sentiment": "positive",
  "sentiment_score": 0.852,
  "confidence": "high",
  "metrics": {
    "word_count": 9,
    "character_count": 52,
    "exclamation_marks": 1,
    "question_marks": 0
  }
}
```

#### 2. Batch Analysis
```bash
POST /batch-analyze
Content-Type: application/json

{
  "texts": [
    "I love this product!",
    "This is terrible",
    "It's okay, nothing special"
  ]
}
```

#### 3. Health Check
```bash
GET /health
```

## 🎨 Supported Emotions

| Emotion | Emoji | Keywords |
|---------|-------|----------|
| Joy | 😊 | happy, joyful, excited, wonderful, amazing |
| Sadness | 😢 | sad, unhappy, depressed, disappointed |
| Anger | 😠 | angry, mad, furious, frustrated |
| Fear | 😨 | scared, afraid, terr