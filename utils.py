import yfinance as yf
import requests
import os
from datetime import date, timedelta
import utils_sentiment

end_date = date.today()
start_date = end_date - timedelta(days=14)
stock_data = {}
stock_history = {}
api_key = os.environ.get("API_KEY_FINANCIALS")


def get_stock_history(ticker):
    """
    Grabs data from yfinance API for stock history
    :return: Two week difference in stock price, in both percentage and total difference
    """
    stock = yf.Ticker(ticker)
    stock_table = stock.history(start=start_date, end=end_date)  # Can be edited for a longer or shorter range
    stock_history[ticker] = stock_table
    try:
        start_price = stock_history[ticker]["Open"][0]
    except IndexError:
        return "Error - Stock not found"
    end_price = stock_history[ticker]["Close"][len(stock_history[ticker]["Close"]) - 1]  # Dataframe is sequential
    return "${:.2f} total difference (from {:.2f} to {:.2f}), {:.2f}% change".format(
        (end_price - start_price), start_price, end_price, (((end_price - start_price) / end_price) * 100))


def get_ebit_ratio(stock_ticker):
    """
    Grabs data from Financial Modeling API ratios dataframe
    """
    url_ebit = f'https://financialmodelingprep.com/api/v3/ratios/{stock_ticker}?apikey={api_key}'
    response_ebit = requests.get(url_ebit)
    data_ebit = response_ebit.json()
    if data_ebit:
        ebit_ratio = data_ebit[0]['ebitPerRevenue']
    else:
        return "Error fetching EBIT ratio - Stock not found"
    return f"{ebit_ratio:.2f}"


def get_ebitda_ratio(stock_ticker):
    """
    Grabs data from Financial Modeling API income statement dataframe
    """
    url_ebitda = f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={api_key}'
    response_ebitda = requests.get(url_ebitda)
    data_ebitda = response_ebitda.json()
    if data_ebitda:
        ebitda_ratio = data_ebitda[0]['ebitdaratio']
    else:
        return "Error fetching EBITDA ratio - Stock not found"
    return f"{ebitda_ratio:.2f}"


def get_current_ratio(stock_ticker):
    """
    Grabs data from Financial Modeling API balance sheet dataframe
    """
    url_current_ratio = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/' \
                        f'{stock_ticker}?apikey={api_key}'
    response_current_ratio = requests.get(url_current_ratio)
    data_current_ratio = response_current_ratio.json()
    if data_current_ratio:
        liabilities = data_current_ratio[0]['totalCurrentLiabilities']
        assets = data_current_ratio[0]['totalAssets']
        current_ratio = assets/liabilities
    else:
        return "Error fetching current ratio - Stock not found"
    return f"{current_ratio:.2f}"


def get_eps(stock_ticker):
    """
    Grabs data from Financial Modeling API income statement dataframe
    :return: Earnings Per Share
    """
    url_eps = f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={api_key}'
    response_eps = requests.get(url_eps)
    data_eps = response_eps.json()
    if data_eps:
        return f"{data_eps[0]['eps']:.2f}"
    else:
        return "Error - Stock not found"


def get_return_assets(stock_ticker):
    """
    Grabs data from Financial Modeling API balance sheet and income statement dataframes
    """
    url_income = f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={api_key}'
    response_income = requests.get(url_income)
    data_income = response_income.json()
    url_assets = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock_ticker}?apikey={api_key}'
    response_assets = requests.get(url_assets)
    data_assets = response_assets.json()
    if data_income:
        net_income = data_income[0]['netIncome']
    else:
        return "Error fetching return rates - Stock not found"
    if data_assets:
        total_assets = data_assets[0]['totalAssets']
    else:
        return "Error fetching asset returns - Stock not found"
    return f"{(net_income/total_assets):.2f}"


def get_return_equity(stock_ticker):
    """
    Grabs data from Financial Modeling API balance sheet and income statement dataframes
    """
    url_income = f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={api_key}'
    response_income = requests.get(url_income)
    data_income = response_income.json()
    url_equity = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock_ticker}?apikey={api_key}'
    response_equity = requests.get(url_equity)
    data_equity = response_equity.json()
    if data_income:
        net_income = data_income[0]['netIncome']
    else:
        return "Error fetching return rates - Stock not found"
    if data_equity:
        stockholder_equity = data_equity[0]['totalStockholdersEquity']
    else:
        return "Error fetching equity returns - Stock not found"
    return f"{(net_income/stockholder_equity):.2f}"


def get_stock_data(ticker):
    """
    Calls all util and utils_sentiment data and formats it into one dictionary, used in data_list
    """
    ticker_data = {
        "ticker": ticker,
        "history": get_stock_history(ticker),
        "headline_sentiment": utils_sentiment.get_headline_sentiment(ticker),
        "ebit": get_ebit_ratio(ticker),
        "ebitda": get_ebitda_ratio(ticker),
        "current_ratio": get_current_ratio(ticker),
        "earnings_per_share": get_eps(ticker),
        "return_on_assets": get_return_assets(ticker),
        "return_on_equity": get_return_equity(ticker)
    }
    return ticker_data


def get_tickers(tickers):
    """
    Separate tickers by comma, make them all uppercase, strip the spaces, and remove non-alphabetic characters
    :return: List format of tickers, in the form of ['AAPL','GOOG', etc]
    """
    ticker_list = [''.join(char for char in ticker.strip().upper() if char.isalpha()) for ticker in tickers.split(',')]
    return ticker_list
