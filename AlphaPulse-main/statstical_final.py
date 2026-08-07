import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use("default")  # To use default plotting style of the matplot lib

file_path = r"/Users/hp/OneDrive/Desktop/Week1_Portfolio_Prices.xlsx"

# To check the existence of file
if not os.path.exists(file_path):
    print("Excel file not found!")
    print("Make sure file path is correct.")
    exit()

try:
    df = pd.read_excel(file_path)
    print("Excel Loaded Successfully")
except PermissionError:
    print("Close the Excel file and run again!")
    exit()


# converting date column into Datetime format
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)  # Converts Date into index respective data
print(df.head())


daily_returns = df.pct_change().dropna()  # To calculate percentage change
# To save daily_variable into csv file
# "C:\Users\hp\Desktop\Alpha_Pulse\Portfolio_Result.xlsx"
daily_returns.to_csv(r"C:\Users\hp\Desktop\Alpha_Pulse\Daily_Returns.csv")
print("Daily Returns Saved")


print("\nStatistical Summary")
print(daily_returns.describe())
trading_days = 252
# To calculate the annual returns
annual_returns = daily_returns.mean() * trading_days
# To calculate the annual risk
annual_risk = daily_returns.std() * np.sqrt(trading_days)
stock_summary = pd.DataFrame({
    "Annual Return": annual_returns,
    "Annual Risk": annual_risk
})
stock_summary.to_csv(r"C:\Users\hp\Desktop\Alpha_Pulse\Stock_Summary.csv")
print("Stock Summary Saved")


weights = np.array([0.25, 0.25, 0.25, 0.25])  # Each Stock having weight of 25%
# To calculate the portfolio return
portfolio_return = np.sum(weights * annual_returns)
cov_matrix = daily_returns.cov() * trading_days  # To Calculate the Covariance
# To calculate portfolio variance
portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
portfolio_risk = np.sqrt(portfolio_variance)  # To calculate the Portfolio risk
portfolio_metrics = pd.DataFrame({
    "Metric": ["Expected Return", "Risk (Volatility)"],
    "Value": [portfolio_return, portfolio_risk]
})
# Exporting the calculated values to the excel form
portfolio_metrics.to_csv(
    r"C:\Users\hp\Desktop\Alpha_Pulse\Portfolio_Result.csv", index=False)
print("\nPortfolio Expected Return:", portfolio_return)
print("Portfolio Risk:", portfolio_risk)

# To creat heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(daily_returns.corr(), annot=True, cmap="coolwarm")
plt.title("Stock Correlation Heatmap")
plt.show()

# To create line plot of date vs price
df.plot(figsize=(12, 6))
plt.title("Stock Price Trend (1 Year)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

# To create line plot
daily_returns.plot(figsize=(12, 6))
plt.title("Daily Returns Trend")
plt.xlabel("Date")

# To create histogram
daily_returns.hist(figsize=(12, 8), bins=50)
plt.suptitle("Return Distribution")
plt.show()

# To calculate cumulative returns
cumulative_returns = (1 + daily_returns).cumprod()
cumulative_returns.plot(figsize=(12, 6))  # To create line plot
plt.title("Growth of ₹1 Investment in Each Stock")
plt.show()

# To calculate the Portfolio Daily returns
portfolio_daily_returns = daily_returns.dot(weights)
# To calculate the portfolio cummulative
portfolio_cumulative = (1 + portfolio_daily_returns).cumprod()
portfolio_cumulative.plot(figsize=(12, 6))
plt.title("Portfolio Growth Over Time")
plt.show()
print("\n ALL ANALYSIS COMPLETED SUCCESSFULLY!")

# MONTE CARLO SIMULATION
print("\nPreparing variables for Monte Carlo Simulation...")

annual_cov = daily_returns.cov() * trading_days
num_portfolios = 10000
risk_free_rate = 0.05
print("Annual Returns and Annual Covariance is Ready")
print("Number of Portfolios:", num_portfolios)
print("Risk Free Rate:", risk_free_rate)

print("\nRunning Monte Carlo Simulation...")


results = np.zeros((3, num_portfolios))
weights_record = []
for i in range(num_portfolios):
    weights = np.random.random(len(annual_returns))
    weights /= np.sum(weights)
    weights_record.append(weights)
    portfolio_return = np.sum(weights * annual_returns)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std
    results[0, i] = portfolio_return
    results[1, i] = portfolio_std
    results[2, i] = sharpe_ratio
print("Simulation Completed")

results_df = pd.DataFrame(results.T, columns=["Return", "Risk", "Sharpe"])

max_sharpe_portfolio = results_df.iloc[results_df["Sharpe"].idxmax()]
min_risk_portfolio = results_df.iloc[results_df["Risk"].idxmin()]
print("\nPortfolio with MAX Sharpe Ratio")
print(max_sharpe_portfolio)
print("\nPortfolio with MIN Risk")
print(min_risk_portfolio)

# Monte Carlo simulation plot
plt.figure(figsize=(10, 6))
plt.scatter(results_df["Risk"], results_df["Return"],
            c=results_df["Sharpe"], cmap="viridis")
plt.colorbar(label="Sharpe Ratio")
plt.xlabel("Risk (Volatility)")
plt.ylabel("Expected Return")
plt.title("Monte Carlo Portfolio Optimization")
plt.scatter(max_sharpe_portfolio["Risk"],
            max_sharpe_portfolio["Return"],
            color="red", s=200, label="Max Sharpe")
plt.scatter(min_risk_portfolio["Risk"],
            min_risk_portfolio["Return"],
            color="blue", s=200, label="Min Risk")
plt.legend()
plt.show()

# To export monte carlo simulation data into excel
results_df.to_csv(
    r"C:\Users\hp\Desktop\Alpha_Pulse\MonteCarlo_Portfolios.csv", index=False)
print("\nMONTE CARLO ANALYSIS COMPLETED!")

confidence_level = 0.95

# Value at Risk calculation
var_95 = np.percentile(portfolio_daily_returns, (1 - confidence_level) * 100)
print("\nVALUE AT RISK (95% CONFIDENCE)")
print(f"1-Day Historical VaR (95%) = {var_95:.4f}")
portfolio_value = 100000
var_95_rupees = -var_95 * portfolio_value
print(f"VaR (95%) in ₹ = {var_95_rupees:.2f}")

# Calculate log returns
log_returns = np.log(df / df.shift(1))
log_returns = log_returns.dropna()

# Calculate historical volatility
historical_volatility = log_returns.std() * np.sqrt(trading_days)
print("Annualized Historical Volatility:")
print(historical_volatility)

# Calculate portfolio volatility
portfolio_returns = log_returns.dot(weights)
portfolio_volatility = portfolio_returns.std() * np.sqrt(252)
print("\nPortfolio Annualized Volatility:")
print(portfolio_volatility)

# Calculate Rolling volatility
rolling_volatility = portfolio_returns.rolling(window=21).std() * np.sqrt(252)
print("\nRolling volatility")
print(rolling_volatility)

rolling_vol_df = rolling_volatility.to_frame(name="Rolling_Volatility_21D")
rolling_vol_df = rolling_vol_df.reset_index()
rolling_vol_df.to_csv(
    r"C:\Users\hp\Desktop\Alpha_Pulse\Rolling_Volatility.csv", index=False)
print("Rolling volatitily saved")


# Ploting the Rolling volatility of 21 days vs date
plt.figure()
rolling_volatility.plot()
plt.title("21-Day Rolling Annualized Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.show()
