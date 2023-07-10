from flask import Flask, render_template, request
import config
import data_collect

app = Flask(__name__)
app.config.from_object(config)


@app.route("/", methods=["GET", "POST"])
def dashboard():
    """
    Master method, takes input from submission and formats chosen data into cards to be displayed on the dashboard
    """
    data_list = []
    if request.method == "POST":
        tickers = data_collect.get_tickers(request.form["ticker"])
        analysis_type = request.form["analysisType"]

        for ticker in tickers:
            if analysis_type == "data":
                ticker_data = data_collect.get_stock_data(ticker)
            elif analysis_type == "sentiment":
                ticker_data = data_collect.get_stock_sentiment(ticker)
            data_list.append(ticker_data)

    return render_template("dashboard.html", data_list=data_list)
