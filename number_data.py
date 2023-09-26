import yfinance as yf
from datetime import date, timedelta


def get_stock_history(ticker):
    """
    Grabs data from yfinance API for stock history
    :return: Two week difference in stock price, in both percentage and total difference
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=14)
    stock = yf.Ticker(ticker)
    stock_table = stock.history(start=start_date, end=end_date)  # Can be edited for a longer or shorter range
    try:
        start_price = stock_table["Open"][0]
    except IndexError:
        return "Error - Stock not found"
    end_price = stock_table["Close"][len(stock_table["Close"]) - 1]  # Dataframe is sequential
    return f"${(end_price - start_price):.2f} total difference (from {start_price:.2f} to {end_price:.2f}), " \
           f"{(((end_price - start_price) / end_price) * 100):.2f}% change"


def get_ebitda_ratio(data_ebitda):
    """
    Grabs data from Financial Modeling API income statement dataframe
    """
    if data_ebitda:
        ebitda_ratio = data_ebitda[0]['ebitdaratio']
    else:
        return "Error - Stock not found"
    return f"{ebitda_ratio:.2f}"


def get_current_ratio(data_current_ratio):
    """
    Grabs data from Financial Modeling API balance sheet dataframe
    """
    if data_current_ratio:
        liabilities = data_current_ratio[0]['totalCurrentLiabilities']
        assets = data_current_ratio[0]['totalAssets']
        try:
            current_ratio = assets/liabilities
        except ZeroDivisionError:
            return "Stock does not report liabilities / no liabilities could be pulled"
    else:
        return "Error - Stock not found"
    return f"{current_ratio:.2f}"


def get_eps(data_eps):
    """
    Grabs data from Financial Modeling API income statement dataframe
    :return: Earnings Per Share
    """
    if data_eps:
        return f"{data_eps[0]['eps']:.2f}"
    else:
        return "Error - Stock not found"


def get_return_assets(data_income, data_assets):
    """
    Grabs data from Financial Modeling API balance sheet and income statement dataframes
    """
    if data_income:
        net_income = data_income[0]['netIncome']
    else:
        return "Error - Stock not found"
    if data_assets:
        total_assets = data_assets[0]['totalAssets']
    else:
        return "Error - Stock not found"
    return f"{(net_income/total_assets):.2f}"


def get_return_equity(data_income, data_equity):
    """
    Grabs data from Financial Modeling API balance sheet and income statement dataframes
    """
    if data_income:
        net_income = data_income[0]['netIncome']
    else:
        return "Error - Stock not found"
    if data_equity:
        stockholder_equity = data_equity[0]['totalStockholdersEquity']
    else:
        return "Error - Stock not found"
    return f"{(net_income/stockholder_equity):.2f}"


def get_debt_equity(data_balance):
    """
    Grabs data from Financial Modeling API balance sheet dataframes
    """
    if data_balance:
        liabilities = data_balance[0]['totalLiabilities']
        stockholderequity = data_balance[0]['totalStockholdersEquity']
    else:
        return "Error - Stock not found"
    return f"{liabilities/stockholderequity:.2f}"


def get_opcash_flow(data_cash_flow):
    """
    Grabs data from Financial Modeling API cash flow dataframes
    """
    if data_cash_flow:
        opcash_flow = data_cash_flow[0]['operatingCashFlow']
    else:
        return "Error - Stock not found"
    return f"{opcash_flow}"


def get_div_yield(data_bal, data_cash, ticker):
    """
    Grabs data from Financial Modeling API balance sheet and cash flow dataframes
    """
    if data_bal:
        stock_num = data_bal[0]['commonStock']
    else:
        return "Error - Stock not found"
    if data_cash:
        div_paid = data_cash[0]['dividendsPaid']*-1
        if div_paid == 0:  # If the stock doesn't pay dividends
            return "0.00%"
    else:
        return "Error - Stock not found"
    ticker_data = yf.Ticker(ticker)
    todays_data = ticker_data.history(period='1d')
    curr_price = todays_data['Close'][0]
    dps = div_paid / stock_num
    return f"{((dps/curr_price)*100):.2f}%"
