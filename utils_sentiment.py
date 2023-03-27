from bs4 import BeautifulSoup
import os
import requests
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
from transformers import pipeline

stock_headlines = {}
api_key = os.environ.get("API_KEY_FINANCIALS")


def analyze_headlines(headlines):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = TFAutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

    sentiment_classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    results = []
    for headline in headlines:
        result = sentiment_classifier(headline)[0]
        results.append({"headline": headline, "sentiment": result["label"], "score": result["score"]})
    return results


def get_headline_sentiment(stock):
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
            pos_neg = -1
        else:
            pos_neg = 1
        recent_sentiment += pos_neg * data['score']
    try:
        return f"{recent_sentiment / len(stock_headlines[stock]):.2f}"
    except ZeroDivisionError:
        return "Error - Stock not found"
