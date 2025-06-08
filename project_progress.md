# Stock Market Project Progress Documentation

## Trial Programs Evolution

### trial_0_nse_analysis.py  
**Input:** Direct NSE data using nespy library  
**Output:** 
- Correlation Heatmap
- Lag Heatmap 

**Description:** Initial attempt at NSE stock analysis with basic correlation study  
**Changes:** Base version

### trial_1_prototype.py  
**Input:** Yahoo Finance data using yfinance  
**Output:** Basic correlation analysis results  
**Description:** Switched to yfinance for more reliable data access  
**Changes:** Changed data source from nespy to yfinance

### trial_2_test_cases.py  
**Input:** Synthetic test data  
**Output:** Correlation test validations  
**Description:** Validation of correlation algorithm using controlled test cases  
**Changes:** Added test cases for algorithm verification

### trial_3_basic_correlation.py  
**Input:** 100 NSE stock price data (2024-01-05 to 2025-01-30)  
**Output:**
- Correlation matrix
- Correlation visualization  

**Description:** First full-scale implementation with actual stock data  
**Changes:** Expanded to 100 stocks, added basic visualizations

### trial_4_lag_analysis.py  
**Input:** NSE stock price time series  
**Output:**
- Correlation Heatmap
- Lag Heatmap  

**Description:** Added temporal analysis with lag relationships  
**Changes:** Introduced lag analysis visualization

### trial_5_visualization.py  
**Input:** NSE stock price data  
**Output:**
- stock_correlation_matrix.csv
- correlation_heatmap.png
- lag_correlation_scatter.png
- top_correlations.png  

**Description:** Enhanced visualization capabilities  
**Changes:** Added multiple visualization types and file exports

### trial_6_categorized_correlation.py  
**Input:** NSE stock data  
**Output:**
- stock_correlation_matrix.csv
- categorized_correlations.csv
- correlation_heatmap.png
- top_correlations.csv  

**Description:** Introduced correlation categorization  
**Changes:** Added correlation categorization system

### trial_7_enhanced_matrix.py  
**Input:** NSE stock data  
**Output:**
- Matrix with NaN diagonals
- Categorized relationships
- Visual correlation map  

**Description:** Improved matrix handling with self-correlation removal  
**Changes:** Added NaN diagonal handling

### trial_8_rolling_correlation.py  
**Input:** Yahoo Finance API direct feed  
**Output:**
- Complete correlation analysis
- 30-day rolling correlations  

**Description:** Added rolling window analysis  
**Changes:** Introduced rolling correlation concept

### trial_9_sector_correlation.py  
**Input:** 75 stocks across 10 sectors  
**Output:**
- Sector-wise correlation CSV files
- Sector-specific heatmaps  

**Description:** First implementation of sector-based analysis  
**Changes:** Added sector categorization

### trial_10_lag_correlation.py  
**Input:** Stock data with multiple lag windows (20,60,120 days)  
**Output:**
- Correlation plots for various lag periods  

**Description:** Comprehensive lag analysis  
**Changes:** Multiple lag period analysis

### trial_11_comprehensive_correlation.py  
**Input:** Stock data with extended analysis parameters  
**Output:**
- Complete correlation matrix
- Categorized correlations
- Visual heatmaps
- Individual pair analysis  

**Description:** Combined previous features into comprehensive analysis  
**Changes:** Integrated multiple analysis types

### trial_12_combined_sector_analysis.py  
**Input:** Stock data with sector information  
**Output:**
- Full correlation analysis
- Sector-wise analysis
- Multiple visualization types 
 
**Description:** Final combined implementation with all features  
**Changes:** Merged sector analysis with comprehensive correlation study

## main.py Analysis
  
**Purpose:** Production-ready implementation combining best features from trials
  
**Key Features:**
1. Efficient data handling with proper error checking
2. Comprehensive correlation analysis
3. Sector-based insights
4. Multiple output formats
5. Optimized visualization

**Improvements over Trials:**
1. Better error handling
2. Optimized code structure
3. Comprehensive documentation
4. Standardized output format
5. Combined sector and general analysis

**Remarks:**
- Successfully integrates learnings from all trials
- Provides both broad market and sector-specific insights
- Maintains good balance between performance and functionality
- Well-documented for future maintenance
- Follows best practices for data analysis and visualization
