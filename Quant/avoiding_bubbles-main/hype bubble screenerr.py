from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt
import time
import yfinance as yf
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed

def detect_bubble_signal(tc, O, D, a, b, c):
    """
    Determine if there's a significant bubble signal
    
    Parameters:
    - tc: Critical time of potential bubble
    - O: Objective function value
    - D: Degree of log-periodic behavior
    - a, b, c: Model parameters
    
    Returns:
    - Signal strength and type (positive/negative bubble)
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
            return 'Negative Bubble', abs(O)
        else:
            return 'Positive Bubble', abs(O)
    
    return None, None

def process_ticker(ticker, START, END, MAX_SEARCHES=25):
    """
    Process a single ticker using LPPLS model and detect potential bubbles
    """
    try:
        # Download ticker data
        yf.pdr_override()
        data = yf.download(ticker, start=START, end=END)
        
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
        bubble_signal, signal_strength = detect_bubble_signal(tc, O, D, a, b, c)
        
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
            plt.suptitle(f'LPPLS Bubble Analysis for {ticker}\n{bubble_signal} (Signal Strength: {signal_strength:.4f})')
            
            # Plot 1: Original Price and Critical Time
            plt.subplot(2, 1, 1)
            plt.plot(data['Date'], data['Adj Close'], label='Adj Close')
            plt.scatter(pd.Timestamp.fromordinal(int(tc)), 
                        data['Adj Close'].iloc[np.abs(time - int(tc)).argmin()], 
                        color='red', label='Critical Time')
            plt.title(f'{ticker} - Price with Critical Time')
            plt.legend()
            
            # Plot 2: Confidence Indicators
            plt.subplot(2, 1, 2)
            lppls_model.plot_confidence_indicators(res)
            plt.title(f'{ticker} - Confidence Indicators')
            
            # Save the plot
            plt.tight_layout()
            plt.savefig(f'{ticker}_bubble_analysis.png')
            plt.close()
            
            # Return bubble information
            return {
                'ticker': ticker,
                'bubble_type': bubble_signal,
                'signal_strength': signal_strength,
                'critical_time': pd.Timestamp.fromordinal(int(tc)),
                'm': m,
                'w': w,
                'a': a,
                'b': b,
                'c': c,
                'O': O,
                'D': D
            }
        
        return None
    
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None

def main():
    # Configuration
    START = '2024-01-01'
    END = '2024-12-04'
    
    # List of tickers to analyze
    tickers = ['NQ=F', 'ES=F', 'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'SPY']
    
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
                    print(f"Bubble detected for {ticker}: {result['bubble_type']} with strength {result['signal_strength']:.4f}")
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

if __name__ == "__main__":
    main()