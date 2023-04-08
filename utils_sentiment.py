from transformers import pipeline
import torch

sentiment_classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english",
                                device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))


def analyze_headlines(headlines):
    results = []
    for headline in headlines:
        result = sentiment_classifier(headline)[0]
        results.append({"headline": headline, "sentiment": result["label"], "score": result["score"]})
    return results


def get_most_negative(sentiments):
    neg = 2
    headline = ""
    for data in sentiments:
        if data['sentiment'] == 'NEGATIVE':
            pos_neg = -1  # all negative sentiments are given a value of score * -1
        else:
            pos_neg = 1  # all positive sentiment are given a value of score * 1
        if neg > pos_neg * data['score']:
            neg = pos_neg * data['score']
            headline = data["headline"]
    return {"headline": headline,
            "score": neg
            }


def get_most_positive(sentiments):
    pos = -2
    headline = ""
    for data in sentiments:
        if data['sentiment'] == 'NEGATIVE':
            pos_neg = -1  # all negative sentiments are given a value of score * -1
        else:
            pos_neg = 1  # all positive sentiment are given a value of score * 1
        if pos < pos_neg * data['score']:
            pos = pos_neg * data['score']
            headline = data["headline"]
    return {"headline": headline,
            "score": pos
            }


def get_headline_sentiment(headlines):
    sentiment_results = analyze_headlines(headlines)
    recent_sentiment = 0
    for data in sentiment_results:
        if data['sentiment'] == 'NEGATIVE':
            pos_neg = -1  # all negative sentiments are given a value of score * -1
        else:
            pos_neg = 1  # all positive sentiment are given a value of score * 1
        recent_sentiment += pos_neg * data['score']
    try:
        return {"sentiment_score": f"{recent_sentiment / len(sentiment_results):.2f}",
                "most_positive_headline": get_most_positive(sentiment_results)['headline'],
                "most_positive_score": f"{get_most_positive(sentiment_results)['score']:.2f}",
                "most_negative_headline": get_most_negative(sentiment_results)['headline'],
                "most_negative_score": f"{get_most_negative(sentiment_results)['score']:.2f}"
                }
    except ZeroDivisionError:
        return "Error - Stock not found"
