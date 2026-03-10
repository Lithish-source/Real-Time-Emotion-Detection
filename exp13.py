from collections import Counter

# Sample dataset of customer reviews
reviews = [
    "This product is very good",
    "Good quality and good performance",
    "This product is not good",
    "Very good product and excellent quality"
]

# Combine all reviews into one string
text = " ".join(reviews)

# Convert text to lowercase and split into words
words = text.lower().split()

# Calculate word frequency
word_freq = Counter(words)

# Display frequency distribution
print("Word Frequency Distribution:")
for word, count in word_freq.items():
    print(word, ":", count)