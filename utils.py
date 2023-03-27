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
    stock = yf.Ticker(ticker)
    stock_table = stock.history(start=start_date, end=end_date)
    stock_history[ticker] = stock_table
    try:
        start_price = stock_history[ticker]["Open"][0]
    except IndexError:
        return "Error - Stock not found"
    end_price = stock_history[ticker]["Close"][len(stock_history[ticker]["Close"]) - 1]
    return "${:.2f} total difference (from {:.2f} to {:.2f}), {:.2f}% change".format(
        (end_price - start_price), start_price, end_price, (((end_price - start_price) / end_price) * 100))


def get_ratios(stock_ticker):
    url_ebit = f'https://financialmodelingprep.com/api/v3/ratios/{stock_ticker}?apikey={api_key}'
    response_ebit = requests.get(url_ebit)
    data_ebit = response_ebit.json()
    url_ebitda = f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={api_key}'
    response_ebitda = requests.get(url_ebitda)
    data_ebitda = response_ebitda.json()
    url_current_ratio = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/' \
                        f'{stock_ticker}?apikey={api_key}'
    response_current_ratio = requests.get(url_current_ratio)
    data_current_ratio = response_current_ratio.json()
    if data_ebit:
        ebit_ratio = data_ebit[0]['ebitPerRevenue']
    else:
        return "Error fetching financial ratios"
    if data_ebitda:
        ebitda_ratio = data_ebitda[0]['ebitdaratio']
    else:
        return "Error fetching financial ratios"
    if data_current_ratio:
        liabilities = data_current_ratio[0]['totalCurrentLiabilities']
        assets = data_current_ratio[0]['totalAssets']
        current_ratio = assets/liabilities
    else:
        return "Error fetching financial ratios"
    return f"EBIT: {ebit_ratio:.2f}\n" \
           f"EBITDA: {ebitda_ratio:.2f}\n" \
           f"Current Ratio: {current_ratio:.2f}"


def get_eps(stock_ticker):
    url_eps = f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={api_key}'
    response_eps = requests.get(url_eps)
    data_eps = response_eps.json()
    if data_eps:
        return f"{data_eps[0]['eps']:.2f}"
    else:
        return "Error fetching income statement"


def get_stock_data(ticker):
    return ticker + f": \n" \
                    f"Two-Week Stock History: {get_stock_history(ticker)} \n" \
                    f"Recent Headline Sentiment: {utils_sentiment.get_headline_sentiment(ticker)} \n" \
                    f"{get_ratios(ticker)} \n" \
                    f"Earnings per Share: {get_eps(ticker)}"


def get_tickers(tickers):
    ticker_list = [ticker.strip() for ticker in tickers.split(',')]
    return ticker_list
