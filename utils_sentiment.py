from bs4 import BeautifulSoup
import requests
import torch
from transformers import pipeline

stock_headlines = {}


def analyze_headlines(headlines):
    """
    Uses pretrained distilbert sentiment analysis model to read headlines and assign them a sentiment score
    :return: Dictionary for a certain stock, with headline, sentiment, and score labels
    """
    sentiment_classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english",
                                    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    results = []
    for headline in headlines:
        result = sentiment_classifier(headline)[0]
        results.append({"headline": headline, "sentiment": result["label"], "score": result["score"]})  # headline could be dropped, I kept it in for interest's sake
    return results


def get_headline_sentiment(stock):
    """
    Grabs headlines using yfinance and BeautifulSoup, then calculates sentiment score
    :return: A numerical value for the recent headline sentiment -1 (most negative) <= x <= 1 (most positive)
    """
    base_url = "https://finance.yahoo.com/quote/{}?p={}".format(stock, stock)
    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, "html.parser")
    headline_elements = soup.find_all("h3", class_="Mb(5px)")
    headlines = []
    for element in headline_elements:
        headlines.append(element.get_text())

    sentiment_results = analyze_headlines(headlines)

    stock_headlines[stock] = sentiment_results
    recent_sentiment = 0
    for data in stock_headlines[stock]:
        if data['sentiment'] == 'NEGATIVE':
            pos_neg = -1  # all negative sentiments are given a value of score * -1
        else:
            pos_neg = 1  # all positive sentiment are given a value of score * 1
        recent_sentiment += pos_neg * data['score']
    try:
        return f"{recent_sentiment / len(stock_headlines[stock]):.2f}"  # average
    except ZeroDivisionError:
        return "Error - Stock not found"
