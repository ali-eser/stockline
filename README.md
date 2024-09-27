# Stockline
#### Video Demo:  <https://youtu.be/oE_DA2k2iC0>
#### Description: CLI asset tracker and stock/currency calculator written in Python 3.11
Stockline is a command line tool written in Python 3.11 for the purpose of calculating stock prices, converting currencies, creating a watchlist using SQL database that allows you to check your portfolio and net worth at any given time.

The program contains six functions excluding main, and is shipped with a database named "assets.db". Stockline uses "dataset", a SQLAlchemy based package that abstracts SQL queries and allows for quick CRUD operations on small databases such as "assets.db". The database contains one table which consists of three columns: id (PRIMARY KEY), symbol (for recording user asset names), and amount (for calculating asset value).

Stockline uses "yfinance" library to get stock prices and exchange rates from Yahoo Finance. This way, neither I have to ship it with an API key, nor users would have to provide their own API keys in order to simply get it functional.
