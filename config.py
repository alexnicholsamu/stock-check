import os

SECRET_KEY = os.environ.get("SECRET_KEY") or ""

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.environ.get("STOCK_MAIL_USERNAME") or ""
MAIL_PASSWORD = os.environ.get("STOCK_MAIL_PASSWORD") or ""
MAIL_DEFAULT_SENDER = ("Stock Dashboard", MAIL_USERNAME)
