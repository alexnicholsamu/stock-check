import requests
import os
import utils
import utils_sentiment
from bs4 import BeautifulSoup


def data_call(ticker):
    api_key = os.environ.get("API_KEY_FINANCIALS")
    url_income_statement = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={api_key}'
    response_income_statement = requests.get(url_income_statement)
    data_income_statement = response_income_statement.json()
    url_balance_sheet = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={api_key}'
    response_balance_sheet = requests.get(url_balance_sheet)
    data_balance_sheet = response_balance_sheet.json()
    url_company_ratios = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={api_key}'
    response_company_ratios = requests.get(url_company_ratios)
    data_company_ratios = response_company_ratios.json()
    return {"Balance Sheet": data_balance_sheet,
            "Income Statement": data_income_statement,
            "Ratios": data_company_ratios}


def get_article_body(article_soup):
    article_body = article_soup.find('article')
    if article_body:
        return article_body.get_text()
    else:
        return None


def get_articles(stock):
    base_url = f"https://finance.yahoo.com/quote/{stock}?p={stock}"
    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, "html.parser")
    headline_elements = soup.find_all("h3", class_="Mb(5px)")

    articles = []
    for element in headline_elements:
        article_url = element.find("a")["href"]

        # Check if URL is relative and convert it to absolute
        if article_url.startswith("/"):
            article_url = "https://finance.yahoo.com" + article_url

        article_page = requests.get(article_url)
        article_soup = BeautifulSoup(article_page.content, "html.parser")

        # Headline
        if element.text:
            headline = element.text
        else:
            headline = "Error - Stock not found"

        # Body text
        body_text = get_article_body(article_soup)
        if body_text is not None:
            body_text = body_text.strip()
        elif not headline == "Error - Stock not found":
            body_text = "This article is a Banner article, i.e. no body text"
        else:
            body_text = "Error - Stock not found"

        articles.append({
            "headline": headline,
            "body_text": body_text
        })

    return articles


def get_stock_data(ticker):
    """
    Calls all util and utils_sentiment data and formats it into one dictionary, used in data_list
    """
    company_data = data_call(ticker)
    ticker_data = {
        "ticker": ticker,
        "analysis_type": "data",
        "history": utils.get_stock_history(ticker),
        "ebit": utils.get_ebit_ratio(company_data["Ratios"]),
        "ebitda": utils.get_ebitda_ratio(company_data["Income Statement"]),
        "current_ratio": utils.get_current_ratio(company_data["Balance Sheet"]),
        "earnings_per_share": utils.get_eps(company_data["Income Statement"]),
        "return_on_assets": utils.get_return_assets(company_data["Income Statement"], company_data["Balance Sheet"]),
        "return_on_equity": utils.get_return_equity(company_data["Income Statement"], company_data["Balance Sheet"])
    }
    return ticker_data


def get_stock_sentiment(ticker):
    articles = get_articles(ticker)
    data = utils_sentiment.get_headline_sentiment(articles)
    ticker_data = {
        "ticker": ticker,
        "analysis_type": "sentiment",
        "headline_sentiment": data["sentiment_score"],
        "most_positive_headline": data["most_positive_headline"],
        "most_positive_score": data["most_positive_score"],
        "most_negative_headline": data["most_negative_headline"],
        "most_negative_score": data["most_negative_score"]
    }
    return ticker_data


def get_tickers(tickers):
    """
    Separate tickers by comma, make them all uppercase, strip the spaces, and remove non-alphabetic characters
    :return: List format of tickers, in the form of ['AAPL','GOOG', etc]
    """
    ticker_list = [''.join(char for char in ticker.strip().upper() if char.isalpha()) for ticker in tickers.split(',')]
    return ticker_list