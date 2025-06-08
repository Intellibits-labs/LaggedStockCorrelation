# Lagged Correlation Analysis of Stock Prices

## 1. Introduction

This project focuses on analyzing the lagged correlations between the closing prices of selected stocks, identifying patterns that could inform investment strategies.

## 2. Objectives

> **Primary Goals:**
- Compute the maximum correlation between pairs of stock closing prices, considering various time lags.
- Identify the specific lag at which the maximum correlation occurs.
- Visualize the correlation patterns to discern potential lead-lag relationships among stocks.

## 3. Methodology

### 3.1 Data Collection

| Component | Description |
|-----------|-------------|
| **Source** | Stock price data from Yahoo Finance (`yfinance` library) |
| **Period** | February 26, 2024 - February 25, 2025 |
| **Stocks** | Selection of major companies across sectors |

### 3.2 Data Processing

**Key Processing Steps:**
1. **Data Retrieval:** 
   - Utilized `yfinance` library
   - Fetched historical closing prices
   
2. **Data Cleaning:**
   - Forward fill for missing values
   - Maintained data continuity
   
3. **Data Alignment:**
   - Based on trading dates
   - Ensured cross-stock consistency

### 3.3 Lagged Correlation Function




```python
import numpy as np
from scipy import stats

def laggedCorr(a, b):
    """
    Calculate the maximum correlation between two series considering different lags.
    Using Spearman rank correlation instead of Pearson.
    Returns the highest correlation value and its corresponding lag.
    Implements improvements to reduce spurious 0-lag results.
    """
    a = np.array(a)
    b = np.array(b)

    # Reduce maximum lag to a more reasonable value based on data size
    max_lag = min(60, len(a) // 10)  # Using 10% of data length as maximum lag

    correlations = []
    lags = []
    p_values = []

    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            # Align series with negative lag
            series_a = a[-lag:]
            series_b = b[:lag]
        elif lag > 0:
            # Align series with positive lag
            series_a = a[:-lag]
            series_b = b[lag:]
        else:
            # No lag
            series_a = a
            series_b = b

        # Only calculate if there's enough data
        if len(series_a) > 10 and len(series_b) > 10:
            # Get both correlation and p-value
            corr_result = stats.spearmanr(series_a, series_b)
            corr = corr_result[0]
            p_val = corr_result[1]

            correlations.append(corr)
            lags.append(lag)
            p_values.append(p_val)
        else:
            # Not enough data for reliable correlation
            correlations.append(0)
            lags.append(lag)
            p_values.append(1.0)

    # Filter for statistical significance
    significant_indices = [i for i, p in enumerate(p_values) if p < 0.05]

    if not significant_indices:
        return 0, 0  # No significant correlation found

    # Among significant correlations, find the one with highest absolute value
    abs_corrs = [abs(correlations[i]) for i in significant_indices]
    max_abs_corr_idx = significant_indices[abs_corrs.index(max(abs_corrs))]

    # Use a bias against selecting lag 0 to overcome the natural preference for lag 0
    # Only select lag 0 if it's significantly better than other lags
    if lags[max_abs_corr_idx] == 0:
        # Find the next best lag that's not 0
        non_zero_indices = [i for i in significant_indices if lags[i] != 0]
        if non_zero_indices:
            next_best_corr = max([abs(correlations[i]) for i in non_zero_indices])
            if abs(correlations[max_abs_corr_idx]) - next_best_corr < 0.05:
                # If lag 0 isn't substantially better, choose non-zero lag
                non_zero_abs_corrs = [abs(correlations[i]) for i in non_zero_indices]
                next_best_idx = non_zero_indices[non_zero_abs_corrs.index(next_best_corr)]
                return correlations[next_best_idx], lags[next_best_idx]

    return correlations[max_abs_corr_idx], lags[max_abs_corr_idx]
```


## 4. Implementation Steps

### 4.1 Data Preparation
1. **Loading Data**
   - CSV file import
   - Date parsing
   - Index setup

2. **Preprocessing**
   - Missing value handling
   - Date alignment
   - Data validation

### 4.2 Analysis Execution
1. **Correlation Computation**
   - Pair-wise analysis
   - Lag calculation
   - Statistical significance testing

2. **Result Processing**
   - Data aggregation
   - Statistical summary
   - Key metric extraction

## 5. Results

### 5.1 Lagged Correlation Findings

#### 5.1.1 Stock Pairs from Same Business Families

**Strong Positive Correlation (>0.6)**

| Stock Pair | Correlation | Lag | Analysis |
|------------|------------|-----|----------|
| ADANIPORTS.NS & ADANIENT.NS | 0.653 | -19 | Core Adani infra businesses |
| ADANIPOWER.NS & ADANIENSOL.NS | 0.652 | -19 | Shared energy vertical |
| TATAMOTORS.NS & TATASTEEL.NS | 0.712 | 19 | Supply chain dependency |
| BAJAJFINSV.NS & BAJFINANCE.NS | 0.699 | -1 | Financial umbrella |
| RELIANCE.NS & JIOFIN.NS | 0.611 | -24 | Ecosystem leverage |

**Weak/Negative Correlation (<0.3)**

| Stock Pair | Correlation | Lag | Analysis |
|------------|------------|-----|----------|
| ADANIPORTS.NS & ADANIGREEN.NS | 0.287 | -17 | Different business cycles |
| TATACONSUM.NS & TATAPOWER.NS | -0.204 | -10 | Defensive vs cyclical |
| BAJAJHLDNG.NS & BAJAJ-AUTO.NS | 0.233 | -24 | Holding vs operational |
| RELIANCE.NS & RELIANCE.NS | Low | N/A | O2C vs Retail segments |
| ADANIENT.NS & ADANIENSOL.NS | 0.274 | -24 | Core vs niche segments |

#### 5.1.2 Key Insights from Business Families

- **Strong Links:** Vertical integration (e.g., Adani ports/power, Tata auto/steel).
- **Weak Links:** Diversified groups (e.g., Tata FMCG vs. energy, Bajaj Auto vs. finance).
- **Lags:** E.g., Adani Ent. leads ports by 19 days, suggesting top-down influence.

### 5.2 Note on High Correlation Values (~0.9)

Several stock pairs showed correlation coefficients close to ±0.9, especially within the banking and IT sectors. This is likely due to the inherent similarity in their macroeconomic drivers—such as interest rates, currency exchange rates, and global economic cycles. Furthermore, the use of Spearman rank correlation emphasizes relative movement patterns rather than absolute price similarity. Therefore, when two stocks consistently move in the same direction—even with different magnitudes—their correlation remains high. These high values are expected in tightly coupled sectors and reflect genuine economic co-movement rather than spurious relationships.

#### 5.2.1 Possible Reasons

- Stocks in the same sector or business group often respond similarly to macroeconomic factors, regulatory changes, and earnings cycles.
- The algorithm used Spearman correlation, which captures rank-order similarity—so even if absolute prices differ, if they rise/fall together consistently, correlation appears high.
- In sectors like banking or IT, companies may move nearly in lockstep due to shared interest rate exposure or global market sensitivity (e.g., HDFC Bank & ICICI Bank).
- Lag bias was reduced in the function, meaning lag-0 wasn’t automatically favored unless it was significantly better.

### 5.3 Visualization

Heatmaps were generated to illustrate the correlation coefficients across different lags for each pair of stocks. These visualizations highlighted clusters of stocks with strong positive or negative correlations, aiding in the identification of potential lead-lag relationships.

## 6. Future Work

### Priority Research Areas:
1. **Alternative Algorithms**
   - Dynamic Time Warping (DTW)
   - Granger Causality Tests
   - Non-linear correlation methods

2. **Dataset Enhancements**
   - Technical indicators
   - Intraday data
   - Volatility metrics
   - Market sentiment data

3. **Advanced Analysis**
   - Rolling window correlation
   - Multi-year analysis
   - Crisis period focus
   - Sector rotation studies

## 7. Conclusion

> This comprehensive analysis of lagged correlations between stock prices has revealed significant patterns and relationships. The findings demonstrate clear lead-lag relationships within business families and across sectors, providing valuable insights for investment strategy development and risk management.

---
**Note:** All correlation values are based on daily closing prices and should be considered alongside other market indicators and fundamental analysis.
