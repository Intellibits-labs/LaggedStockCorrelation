import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

def laggedCorr(a, b, max_lag=20):
    """
    Calculate the maximum correlation between two series considering different lags.
    
    Args:
        a, b: numpy arrays of same length containing the time series data
        max_lag: Maximum lag to consider (default: 20)
        
    Returns:
        float: Maximum correlation coefficient found across all lags
        int: Lag at which the maximum correlation occurs
    """
    a = np.array(a)
    b = np.array(b)
    
    correlations = []
    lags = []
    
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            corr = stats.pearsonr(a[-lag:], b[:lag])[0]
        elif lag > 0:
            corr = stats.pearsonr(a[:-lag], b[lag:])[0]
        else:
            corr = stats.pearsonr(a, b)[0]
        correlations.append(corr)
        lags.append(lag)
    
    max_corr = max(correlations, key=abs)
    max_lag_index = correlations.index(max_corr)
    
    return max_corr, lags[max_lag_index]

# Read the stock data from CSV file
data = pd.read_csv('inputs/stocks.csv', parse_dates=['Date'])


# Set the Date column as index
data.set_index('Date', inplace=True)

# Fill missing values using forward fill, then backward fill
data.ffill(inplace=True)
data.bfill(inplace=True)

# Check if any NaNs still exist (for debugging)
print("Remaining NaN values:", data.isnull().sum().sum())  # Should print 0

# Get the list of stock tickers (column names)
tickers = data.columns.tolist()

results = []

# Calculate lagged correlations for all pairs of stocks
for i in range(len(tickers)):
    for j in range(i + 1, len(tickers)):
        stock_a = data.iloc[:, i]
        stock_b = data.iloc[:, j]
        corr, lag = laggedCorr(stock_a.values, stock_b.values)
        results.append((tickers[i], tickers[j], corr, lag))

# Display the results
print("All Lagged Correlations:")
for stock_a, stock_b, corr, lag in results:
    print(f"{stock_a} and {stock_b}: Correlation = {corr:.2f}, Lag = {lag} days")

# Identify negatively correlated, no correlation, and strongly correlated pairs
negatively_correlated = [(stock_a, stock_b, corr, lag) for stock_a, stock_b, corr, lag in results if corr < -0.5]
positively_correlated = [(stock_a, stock_b, corr, lag) for stock_a, stock_b, corr, lag in results if corr > 0.5]
no_correlation = [(stock_a, stock_b, corr, lag) for stock_a, stock_b, corr, lag in results if -0.1 <= corr <= 0.1]

print("\nStrongly Negatively Correlated Pairs (correlation < -0.5):")
for stock_a, stock_b, corr, lag in sorted(negatively_correlated, key=lambda x: x[2]):
    print(f"{stock_a} and {stock_b}: Correlation = {corr:.2f}, Lag = {lag} days")

print("\nStrongly Positively Correlated Pairs (correlation > 0.5):")
for stock_a, stock_b, corr, lag in sorted(positively_correlated, key=lambda x: x[2], reverse=True):
    print(f"{stock_a} and {stock_b}: Correlation = {corr:.2f}, Lag = {lag} days")

print("\nNo Correlation Pairs (-0.1 ≤ correlation ≤ 0.1):")
for stock_a, stock_b, corr, lag in no_correlation:
    print(f"{stock_a} and {stock_b}: Correlation = {corr:.2f}, Lag = {lag} days")

# Create a DataFrame for correlation matrix (without self-correlations)
correlation_matrix = pd.DataFrame(index=tickers, columns=tickers)

# Fill the correlation matrix, but keep diagonal as NaN to exclude self-correlations
for stock_a, stock_b, corr, lag in results:
    correlation_matrix.loc[stock_a, stock_b] = corr
    correlation_matrix.loc[stock_b, stock_a] = corr  # Symmetric matrix

# Convert the correlation matrix to numeric (diagonals remain NaN)
correlation_matrix = correlation_matrix.astype(float)

# Save the correlation matrix to a CSV file
correlation_matrix.to_csv('stock_correlation_matrix.csv')

# Create a mask for the heatmap to hide self-correlations
mask = np.eye(len(tickers), dtype=bool)

# Save categorized correlation results
categorized_results = pd.DataFrame(results, columns=['Stock A', 'Stock B', 'Correlation', 'Lag'])
categorized_results['Category'] = categorized_results['Correlation'].apply(
    lambda x: 'Positive' if x > 0.5 else ('Negative' if x < -0.5 else 'No Correlation')
)
categorized_results.to_csv('categorized_correlations.csv', index=False)

# Plot the correlation heatmap with masked diagonal
plt.figure(figsize=(20, 16))
sns.heatmap(correlation_matrix, cmap='coolwarm', center=0, 
            xticklabels=True, yticklabels=True, mask=mask)
plt.title('Correlation Heatmap between NSE Stocks (Self-Correlations Removed)')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300)
plt.close()

# Find the top correlations (excluding self-correlations)
flat_corr = []
for i in range(len(tickers)):
    for j in range(i+1, len(tickers)):  # This already excludes self-correlations (i,i)
        flat_corr.append((tickers[i], tickers[j], correlation_matrix.iloc[i, j]))

# Sort by absolute correlation
top_correlations = sorted(flat_corr, key=lambda x: abs(x[2]), reverse=True)[:20]

# Create a DataFrame for top correlations
top_corr_df = pd.DataFrame(top_correlations, columns=['Stock A', 'Stock B', 'Correlation'])
top_corr_df['AbsCorrelation'] = top_corr_df['Correlation'].abs()
top_corr_df.sort_values('AbsCorrelation', ascending=False, inplace=True)

# Save the top correlations to a CSV file
top_corr_df.to_csv('top_correlations.csv', index=False)

print("\nAnalysis complete. Output files saved:")
print("1. stock_correlation_matrix.csv - Full correlation matrix (with NaN diagonals)")
print("2. categorized_correlations.csv - Categorized correlations (Positive, Negative, No Correlation)")
print("3. correlation_heatmap.png - Heatmap visualization of correlations (self-correlations removed)")
print("4. top_correlations.csv - Top 20 stock correlations by absolute value")

print("\nStarting sector-based analysis...")

# Define sectors for each company
df_sectors = {
    "Financials": ["SHRIRAMFIN.NS", "BAJAJHLDNG.NS", "CHOLAFIN.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "INDUSINDBK.NS", "HDFCBANK.NS", "AXISBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "BANKBARODA.NS", "PNB.NS", "UNIONBANK.NS"],
    "Technology": ["INFY.NS", "TCS.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS", "LTIM.NS"],
    "Pharmaceuticals": ["SUNPHARMA.NS", "TORNTPHARM.NS", "CIPLA.NS", "DRREDDY.NS", "ZYDUSLIFE.NS", "DIVISLAB.NS", "APOLLOHOSP.NS"],
    "Consumer Goods": ["ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "TATACONSUM.NS", "BRITANNIA.NS", "DABUR.NS", "GODREJCP.NS", "UNITDSPR.NS"],
    "Energy": ["RELIANCE.NS", "ONGC.NS", "GAIL.NS", "NTPC.NS", "TATAPOWER.NS", "ADANIGREEN.NS", "ADANIPOWER.NS", "JSWENERGY.NS"],
    "Automobiles": ["TATAMOTORS.NS", "EICHERMOT.NS", "TVSMOTOR.NS", "HEROMOTOCO.NS", "MARUTI.NS", "M&M.NS", "BAJAJ-AUTO.NS", "MOTHERSON.NS"],
    "Infrastructure": ["L&T.NS", "DLF.NS", "GRASIM.NS", "ULTRACEMCO.NS", "SHREECEM.NS", "AMBUJACEM.NS", "SIEMENS.NS", "ABB.NS", "HAVELLS.NS", "BHEL.NS"],
    "Metals": ["HINDALCO.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "JINDALSTEL.NS", "VEDL.NS"],
    "Telecommunications": ["BHARTIARTL.NS", "JIOFIN.NS"],
    "Miscellaneous": ["ZOMATO.NS", "NAUKRI.NS", "INDIGO.NS", "TRENT.NS", "IRCTC.NS", "LODHA.NS", "VBL.NS"]
}

def calculate_sector_correlation(data, sector_stocks):
    """Calculates lagged correlation matrix for a given sector."""
    sector_data = data[sector_stocks].dropna()
    results = []
    for i in range(len(sector_stocks)):
        for j in range(i + 1, len(sector_stocks)):
            stock_a, stock_b = sector_stocks[i], sector_stocks[j]
            corr, lag = laggedCorr(sector_data[stock_a], sector_data[stock_b])
            results.append((stock_a, stock_b, corr, lag))
    return results

# Calculate and save correlation matrices for each sector
for sector, stocks in df_sectors.items():
    available_stocks = [stock for stock in stocks if stock in data.columns]
    if available_stocks:
        lagged_results = calculate_sector_correlation(data, available_stocks)
        
        # Save results
        df_lagged = pd.DataFrame(lagged_results, columns=['Stock A', 'Stock B', 'Correlation', 'Lag'])
        df_lagged.to_csv(f'outputs/sector_based/{sector}_lagged_correlation.csv', index=False)

        # Plot heatmap
        correlation_matrix = df_lagged.pivot(index='Stock A', columns='Stock B', values='Correlation')
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, cmap='coolwarm', annot=True, fmt='.2f')
        plt.title(f'Lagged Correlation Matrix - {sector}')
        plt.savefig(f'outputs/sector_based/{sector}_lagged_correlation_heatmap.png')
        plt.close()

print("Sector-wise lagged correlation analysis complete. Files saved.")