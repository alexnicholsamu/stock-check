# stock-check, a Stock Analysis Dashboard by Alexander Nichols

## Tools used in the creation of this project:

> [Financial Modeling Prep API](https://site.financialmodelingprep.com/) 

> GPT-4 by OpenAI
 
> PyTorch, BeautifulSoup4, yfinance, FLASK, gunicorn 

## Summary:

This is my stock dashboard, where with the input of stock ticker(s) of interest, a user will get access to a full 
wealth of formatted and calculated data of which to make decisions about the stock(s)

Using the _Financial Modeling Prep API_ and _yfinance_, I gather stock data from their balance sheets, income statements, 
and Yahoo! Finance. I also use a pretrained sentiment analysis neural network, called _distilbert_, to analyze stock 
headlines and provide a sentiment score. 

The licence can be found in [LICENSE](LICENSE.md). This can only be hosted locally through running 
[app_run](app_run.py). To run this locally on your machine, you'll need to provide a FLASK secret key to the 
[config](config.py), as well as an API key to the aforementioned _Financial Modeling Prep API_ in [utils](utils.py). 
You can manually enter these into your code in place of environmental variables in the two aforementioned files, 
however I wouldn't recommend that for security reasons unless you are only running the code and not developing it to be 
later published (in line with the [LICENSE](LICENSE.md))

All provided files are necessary to run this.

Future work includes providing more data, as well as the website improvements. Any questions or suggestions should be 
emailed to _alexander.k.nichols@gmail.com_.