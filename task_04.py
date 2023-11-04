# -*- coding: utf-8 -*-
"""Task - 04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Fydxcm9P3lOzZ6tuDl2MLvQ4u-gX5IM4

**PRODIGY INFOTECH**

**Author: Mansi Jadhav**

**Data Science Intern**

Task - 04: Analyze and visualize sentiment patterns in social media data to understand public opinion and attitudes towards specific topics or brands.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import files
upload= files.upload()

df = pd.read_csv('/content/twitter_training.csv')

df.head()

#Checking shape of the dataset
print("Rows: ", df.shape[0])
print("Columns: ", df.shape[1])

df.columns

df.info()

df.isnull()

df.isnull().sum()         #check for missing values

df = df.dropna()      #drop rows with missing values

df.isnull().sum()

# Check for duplicate rows
duplicates = df.duplicated().sum()
print("Number of duplicate rows:", duplicates)

# Remove duplicates
df = df.drop_duplicates()

df['Sentiment'].value_counts()

sentiment_counts = [21698, 19713, 17707, 12537]
sentiments = ['Negative', 'Positive', 'Neutral', 'Irrelevant']
plt.figure(figsize=(8, 8))
plt.pie(sentiment_counts, labels=sentiments, autopct='%1.1f%%', startangle=140)
plt.title('Sentiment Distribution')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

"""TEXT CLEANING"""

import re
import nltk
import spacy
nltk.download ('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize

def clean_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove mentions and hashtags
    text = re.sub(r'@\w+|\#', '', text)

    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]

    return ' '.join(words)

# Apply the cleaning function to the "Tweet Content" column
df['Cleaned Tweet'] = df['Tweet_Content'].apply(clean_text)

"""FEATURE ENGINEERING"""

from textblob import TextBlob

# Extract hashtags
df['Hashtags'] = df['Tweet_Content'].apply(lambda x: re.findall(r'#\w+', x))

# Calculate sentiment scores using TextBlob
df['SentimentScore'] = df['Cleaned Tweet'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Sentiment Analysis using NLTK VADER
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
df['SentimentScore'] = df['Tweet_Content'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
df['Sentiment'] = df['SentimentScore'].apply(lambda score: 'positive' if score > 0 else ('negative' if score < 0 else 'neutral'))

sentiment_counts = df['Sentiment'].value_counts()
sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Create a Word Cloud
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Tweet_Content']))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Tweets')
plt.show()

#Grouped bar chart of comparison of entities
sns.countplot(data=df, x='Entity', hue='Sentiment')
plt.title('Sentiment by Entity')
plt.xlabel('Entity')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Sentiment')
plt.show()

import numpy as np
sentiment_scores = {'Positive': 0.6, 'Negative': 0.2, 'Neutral': 0.2}

categories = list(sentiment_scores.keys())
values = list(sentiment_scores.values())

fig, ax = plt.subplots(figsize=(6, 6))

# Create a radar chart
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
values += values[:1]
angles += angles[:1]
ax.fill(angles, values, 'b', alpha=0.1)

# Set the labels for the radar chart
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)

plt.title('Sentiment Radar Chart')
plt.show()

"""ENCODING TARGET COLUMN"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['Sentiment'] = le.fit_transform(df['Sentiment'])

df.head(5)

#Split the data into train & test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df['Cleaned Tweet'], df['Sentiment'], test_size=0.2, random_state=42, stratify=df['Sentiment'])

print("Shape of X_train: ", X_train.shape)
print("Shape of X_test: ", X_test.shape)

"""MACHINE LEARNING MODEL

NAIVE BAYES MODEL
"""

# Create classifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
clf = Pipeline([
    ('vectorizer_tri_grams', TfidfVectorizer()),
    ('naive_bayes', (MultinomialNB()))
])

# Model training
clf.fit(X_train, y_train)

# Get prediction
y_pred = clf.predict(X_test)
y_pred

# Print score
from sklearn.metrics import accuracy_score, classification_report
print(accuracy_score(y_test, y_pred))

# Print classification report
print(classification_report(y_test, y_pred))