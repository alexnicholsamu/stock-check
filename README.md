# stock-check, a Stock Analysis Dashboard, by Alexander Nichols

## Tools used in the creation of this project:

> [Financial Modeling Prep API](https://site.financialmodelingprep.com/) 

> GPT-4 by OpenAI

> Heroku Web Services

## Summary:

This is my stock dashboard, where with the input of only a destination email and stock ticker(s) of interest, 
a user will get access to a full wealth of formatted and calculated data of which to make decisions about the stock

Using the _Financial Modeling Prep API_ and _yfinance_, I gather stock data from their balance sheets, income statements, 
and Yahoo! Finance. I also use a pretrained sentiment analysis neural network, called _distilbert_, to analyze stock 
headlines and provide a sentiment score. 

The licence can be found in [here](LICENSE.md), any non-default libraries/dependencies can be found in 
[the buildpack](requirement.txt). As of 27/03/23, this can only be hosted locally through running [main](wsgi.py). 
To run this locally on your machine, you'll need to provide an email, email password, and FLASK secret key to 
the [config](config.py), as well as an API key to the aforementioned _Financial Modeling Prep API_ in 
[utils_sentiment](utils_sentiment.py). For security reasons, store these as environmental variables in your OS
(as I've done in my code). All the files are necessary to run this, except for [Procfile](Procfile) and 
[the buildpack](requirements.txt) which exists due to my attempts to host this on Heroku.

Future work will hopefully be done to host this on a server to be accessible via the internet (and you won't need to 
add all your data in as described above to use!). Future work includes providing more data, as well as the website 
hosting. Any questions or suggestions should be emailed to _alexander.k.nichols@gmail.com_.