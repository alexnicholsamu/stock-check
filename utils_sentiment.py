import requests
from bs4 import BeautifulSoup
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

stock_headlines = {}

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
ort_session = ort.InferenceSession("model.onnx")


def process_logits(logits):
    labels = ["NEGATIVE", "POSITIVE"]
    probabilities = softmax(logits)
    index = np.argmax(probabilities)
    label = labels[index]
    score = probabilities[0][index]
    return label, score


def softmax(logits):
    exp_logits = np.exp(logits)
    return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)


def analyze_headlines(headlines):
    results = []
    for headline in headlines:
        inputs = tokenizer(headline, return_tensors="np", padding=True, truncation=True)
        logits = ort_session.run(None, {ort_session.get_inputs()[0].name: inputs["input_ids"],
                                        ort_session.get_inputs()[1].name: inputs["attention_mask"]})
        label, score = process_logits(logits)
        results.append({"headline": headline, "sentiment": label, "score": score})
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
