from textblob import TextBlob
import numpy as np

def sentiment(text):
    return TextBlob(text).sentiment.polarity

def volatility(price):
    return abs(price % 5)

def predict(sentiment_score, vol):
    if sentiment_score > 0.2 and vol < 2:
        return "BUY", 0.8
    elif sentiment_score < -0.2:
        return "SELL", 0.75
    return "HOLD", 0.6

def brokerage(price):
    return price * 0.003