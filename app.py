from flask import Flask, render_template, request
from flask_mail import Mail, Message
import config
import utils

app = Flask(__name__)
app.config.from_object(config)

mail = Mail(app)


def send_email(data, recipient):
    subject = f"Stock Data:"
    body = f"Data: \n" \
           f" \n" \
           f"{data}"
    msg = Message(subject, recipients=[recipient], body=body)
    mail.send(msg)


@app.route("/", methods=["GET", "POST"])
def dashboard():
    data = ""
    if request.method == "POST":
        tickers = utils.get_tickers(request.form["ticker"])
        for ticker in tickers:
            ticker_data = utils.get_stock_data(ticker)
            ticker_data += f"\n" \
                           f"\n" \
                           f"\n"
            data += ticker_data

        recipient = request.form["email"]
        send_email(data, recipient)

    return render_template("dashboard.html", data=data)
