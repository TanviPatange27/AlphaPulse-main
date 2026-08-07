import yfinance as yf
import pandas as pd
import os

stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS"]

data = yf.download(
    tickers=stocks,
    period="1y",
    auto_adjust=False,
    progress=False
)

adj_close_prices = data.loc[:, ("Adj Close", slice(None))]
adj_close_prices.columns = adj_close_prices.columns.droplevel(0)

adj_close_prices = adj_close_prices.dropna().reset_index()
adj_close_prices["Date"] = adj_close_prices["Date"].dt.date

adj_close_prices.columns = ["Date", "RELIANCE", "TCS", "HDFCBANK", "INFY"]
adj_close_prices[["RELIANCE", "TCS", "HDFCBANK", "INFY"]] = adj_close_prices[[
    "RELIANCE", "TCS", "HDFCBANK", "INFY"]].round(0)

adj_close_prices.to_excel("Week1_Portfolio_Prices_1Y_Clean.xlsx", index=False)
print("Saved at:", os.getcwd())
