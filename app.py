from flask import Flask, render_template, request
import config
import utils

app = Flask(__name__)
app.config.from_object(config)


@app.route("/", methods=["GET", "POST"])
def dashboard():
    """
    Master method, gathers data from utils and formats it into cards to be displayed on the dashboard
    """
    data_list = []
    if request.method == "POST":
        tickers = utils.get_tickers(request.form["ticker"])  # can deal with all upper/lower cases, spaces,
        for ticker in tickers:
            ticker_data = utils.get_stock_data(ticker)
            data_list.append(ticker_data)

    return render_template("dashboard.html", data_list=data_list)
