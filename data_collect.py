import requests
import os
import number_data
import sentiment_summary
from bs4 import BeautifulSoup


def data_call(ticker):
    """
    :return: use financial modeling prep api to access income statement, balance sheet, and relevant ratios for a stock
    """
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
    url_cash_flow = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?apikey={api_key}'
    response_cash_flow = requests.get(url_cash_flow)
    data_cash_flow = response_cash_flow.json()
    return {"Balance Sheet": data_balance_sheet,
            "Income Statement": data_income_statement,
            "Ratios": data_company_ratios,
            "Cash Flow": data_cash_flow}


def get_headlines(stock):
    """
    :return: scrapes headlines from Yahoo! Finance using beautifulsoup4
    """
    base_url = f"https://finance.yahoo.com/quote/{stock}?p={stock}"
    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, "html.parser")
    headline_elements = soup.find_all("h3", class_="Mb(5px)")

    headlines = []
    for element in headline_elements:
        if element.text:
            headline = element.text
        else:
            headline = "Error - Stock not found"
        headlines.append(headline)

    return headlines


def get_stock_data(ticker):
    """
    Calls all utils data and formats it into one dictionary
    """
    company_data = data_call(ticker)
    ticker_data = {
        "ticker": ticker,
        "analysis_type": "data",
        "history": number_data.get_stock_history(ticker),
        "ebit": number_data.get_ebit_ratio(company_data["Ratios"]),
        "ebitda": number_data.get_ebitda_ratio(company_data["Income Statement"]),
        "current_ratio": number_data.get_current_ratio(company_data["Balance Sheet"]),
        "earnings_per_share": number_data.get_eps(company_data["Income Statement"]),
        "return_on_assets": number_data.get_return_assets(company_data["Income Statement"], company_data["Balance Sheet"]),
        "return_on_equity": number_data.get_return_equity(company_data["Income Statement"], company_data["Balance Sheet"]),
        "debt_equity_ratio": number_data.get_debt_equity(company_data["Balance Sheet"]),
        "op_cash_flow": number_data.get_opcash_flow(company_data["Cash Flow"]),
        "dividend_yield": number_data.get_div_yield(company_data["Balance Sheet"], company_data["Cash Flow"], ticker)
    }
    return ticker_data


def get_stock_sentiment(ticker):
    """
    Calls all utils_sentiment data
    """
    headlines = get_headlines(ticker)
    data = sentiment_summary.get_headline_sentiment(headlines)
    try:
        sentiment_score = data["sentiment_score"]
    except TypeError:  # If the stock is invalid, data["sentiment_score"] will throw a TypeError
        return {
            "ticker": ticker,
            "analysis_type": "sentiment",
            "headline_sentiment": "Error - Stock not found",
            "most_positive_headline": "Error - Stock not found",
            "most_positive_score": "Error - Stock not found",
            "most_positive_headline_summary": "Error - Stock not found",
            "most_negative_headline": "Error - Stock not found",
            "most_negative_score": "Error - Stock not found",
            "most_negative_headline_summary": "Error - Stock not found"
        }
    ticker_data = {
        "ticker": ticker,
        "analysis_type": "sentiment",
        "headline_sentiment": sentiment_score,
        "most_positive_headline": data["most_positive_headline"],
        "most_positive_score": data["most_positive_score"],
        "most_positive_headline_summary": data["most_positive_headline_summary"],
        "most_negative_headline": data["most_negative_headline"],
        "most_negative_score": data["most_negative_score"],
        "most_negative_headline_summary": data["most_negative_headline_summary"]
        }
    return ticker_data


def get_tickers(tickers):
    """
    Separate tickers by comma, make them all uppercase, strip the spaces, and remove non-alphabetic characters
    """
    ticker_list = [''.join(char for char in ticker.strip().upper() if char.isalpha()) for ticker in tickers.split(',')]
    return ticker_list
