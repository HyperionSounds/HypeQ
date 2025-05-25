from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt
import time
import yfinance as yf
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed

def detect_bubble_signal(O, D, a, b):
    """
    Determine if there's a significant bubble signal
    
    Parameters:
    - O: Objective function value
    - D: Degree of log-periodic behavior
    - a: Amplitude parameter
    - b: Second parameter related to oscillations
    
    Returns:
    - Bubble signal type (Positive/Negative/None)
    """
    # Criteria for bubble detection
    bubble_criteria = {
        'objective_threshold': 0.1,  # Lower values indicate better fit
        'degree_threshold': 0.5,     # Higher values suggest stronger log-periodic behavior
        'amplitude_threshold': 0.1   # Significant amplitude of oscillations
    }
    
    # Check if signal meets bubble detection criteria
    if (O < bubble_criteria['objective_threshold'] and 
        D > bubble_criteria['degree_threshold'] and 
        abs(a) > bubble_criteria['amplitude_threshold']):
        # Determine bubble direction based on 'b' parameter
        if b < 0:
            return 'Negative Bubble'
        else:
            return 'Positive Bubble'
    
    return None

def process_ticker(ticker, START, END, MAX_SEARCHES=25):
    """
    Process a single ticker using LPPLS model and detect potential bubbles
    """
    try:
        # Download ticker data
        data = yf.download(ticker, start=START, end=END)
        
        # Check if data is empty
        if data.empty:
            print(f"No data available for {ticker}")
            return None
        
        # Reset index to make Date a column
        data = data.reset_index()
        
        # Convert time to ordinal
        time = [pd.Timestamp.toordinal(t1) for t1 in data['Date']]
        
        # Create log price (handle potential zero or negative values)
        price = np.log(np.maximum(data['Adj Close'].values, 1e-10))
        
        # Create observations array
        observations = np.array([time, price])
        
        # Instantiate LPPLS model
        lppls_model = lppls.LPPLS(observations=observations)
        
        # Fit the model
        tc, m, w, a, b, c, c1, c2, O, D = lppls_model.fit(MAX_SEARCHES)
        
        # Detect bubble signal
        bubble_signal = detect_bubble_signal(O, D, a, b)
        
        # If bubble signal detected, process and plot
        if bubble_signal:
            # Compute confidence indicators
            res = lppls_model.mp_compute_nested_fits(
                workers=1,
                window_size=120, 
                smallest_window_size=30, 
                outer_increment=1, 
                inner_increment=5, 
                max_searches=25
            )
            
            # Create figure for plots
            plt.figure(figsize=(15, 10))
            plt.suptitle(f'{ticker} - {bubble_signal} Detection')
            
            # Plot 1: Model Fit
            plt.subplot(2, 1, 1)
            lppls_model.plot_fit()
            plt.title(f'{ticker} - LPPLS Model Fit')
            
            # Plot 2: Confidence Indicators
            plt.subplot(2, 1, 2)
            lppls_model.plot_confidence_indicators(res)
            plt.title(f'{ticker} - Confidence Indicators')
            
            # Tight layout and show
            plt.tight_layout()
            
            # Return bubble information
            return {
                'ticker': ticker,
                'bubble_type': bubble_signal,
                'critical_time': pd.Timestamp.fromordinal(int(tc)),
                'objective_value': O,
                'periodicity_degree': D
            }
        
        return None
    
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None

def main():
    # Configuration
    START = '2022-01-01'
    END = '2024-12-14'
    
    # List of tickers to analyze
    tickers = [
        'SMH',  # Semiconductor ETF
        'XLK',  # Technology Select Sector SPDR Fund
        'QQQ',  # Nasdaq-100 ETF
        'VGT',  # Vanguard Information Technology ETF
        'SOXX',  # iShares Semiconductor ETF
        'FTEC',  # Fidelity MSCI Information Technology Index ETF
        'IGM',   # iShares Expanded Tech Sector ETF
        'ARKK'   # ARK Innovation ETF
    ]
    
    # Store results
    bubble_results = []
    
    # Use ProcessPoolExecutor for multiprocessing
    with ProcessPoolExecutor(max_workers=3) as executor:
        # Submit jobs for each ticker
        future_to_ticker = {executor.submit(process_ticker, ticker, START, END): ticker for ticker in tickers}
        
        # Collect results
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                result = future.result()
                if result:
                    bubble_results.append(result)
                    print(f"Bubble detected for {ticker}: {result['bubble_type']}")
            except Exception as e:
                print(f"Unexpected error for {ticker}: {e}")
    
    # Create a DataFrame of bubble results
    if bubble_results:
        results_df = pd.DataFrame(bubble_results)
        print("\nBubble Analysis Results:")
        print(results_df)
        
        # Optional: Save results to CSV
        results_df.to_csv('bubble_analysis_results.csv', index=False)
    else:
        print("No bubble signals detected.")
    
    # Show plots for detected bubbles
    plt.show()

if __name__ == "__main__":
    main()