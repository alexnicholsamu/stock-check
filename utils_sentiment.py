from transformers import pipeline, PegasusTokenizer, PegasusForConditionalGeneration
import torch

sentiment_classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english",
                                device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)


def summarize(headline):
    """
    :return: pegasus regeneration of headline summary
    """
    input_ids = tokenizer.encode("summarize: " + headline, return_tensors="pt", max_length=2048, truncation=True)
    summary_ids = model.generate(input_ids, num_beams=4, min_length=16, max_length=48, early_stopping=True,
                                 temperature=1.0)  # I wanted this to reword headline summaries, so it can possibly provide more information
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def analyze_headlines(headlines):
    """
    :return: dictionary of distilbert analysis of headlines
    """
    results = []
    for headline in headlines:
        result = sentiment_classifier(headline)[0]
        results.append({"headline": headline, "sentiment": result["label"], "score": result["score"]})
    return results


def get_most_negative(sentiments):
    """
    :param sentiments: takes sentiment results
    :return: headline and score of most negative headline
    """
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
    """
    :param sentiments: takes sentiment results
    :return: headline and score of most positive headline
    """
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
    """
    :return: master method of sentiment analysis, averages the scores of the headlines and accesses the data from the other methods
    """
    sentiment_results = analyze_headlines(headlines)
    recent_sentiment = 0
    for data in sentiment_results:
        if data['sentiment'] == 'NEGATIVE':
            pos_neg = -1  # all negative sentiments are given a value of score * -1
        else:
            pos_neg = 1  # all positive sentiment are given a value of score * 1
        recent_sentiment += pos_neg * data['score']
    pos_results = get_most_positive(sentiment_results)
    neg_results = get_most_negative(sentiment_results)
    try:
        return {"sentiment_score": f"{recent_sentiment / len(sentiment_results):.2f}",
                "most_positive_headline": pos_results['headline'],
                "most_positive_score": f"{pos_results['score']:.2f}",
                "most_positive_headline_summary": summarize(pos_results['headline']),
                "most_negative_headline": neg_results['headline'],
                "most_negative_score": f"{neg_results['score']:.2f}",
                "most_negative_headline_summary": summarize(neg_results['headline'])
                }
    except ZeroDivisionError:
        return "Error - Stock not found"  # If the stock ticker isn't valid, len(sentiment_results) will be 0
