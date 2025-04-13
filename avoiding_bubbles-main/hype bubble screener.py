from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt
import time
import yfinance as yf
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_ticker(ticker, START, END, MAX_SEARCHES=25):
    """
    Process a single ticker using LPPLS model
    
    Parameters:
    - ticker: Stock ticker symbol
    - START: Start date for data
    - END: End date for data
    - MAX_SEARCHES: Maximum number of searches for LPPLS model
    
    Returns:
    - Tuple with ticker and processing results
    """
    try:
        # Download ticker data
        yf.pdr_override()  # Reset any potential caching issues
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
        
        # Compute confidence indicators
        res = lppls_model.mp_compute_nested_fits(
            workers=1,  # Reduce to avoid multiprocessing issues
            window_size=120, 
            smallest_window_size=30, 
            outer_increment=1, 
            inner_increment=5, 
            max_searches=25
        )
        
        # Create figure for plots
        plt.figure(figsize=(15, 10))
        plt.suptitle(f'LPPLS Analysis for {ticker}')
        
        # Plot 1: Model Fit
        plt.subplot(2, 1, 1)
        lppls_model.plot_fit()
        plt.title(f'{ticker} - LPPLS Model Fit')
        
        # Plot 2: Confidence Indicators
        plt.subplot(2, 1, 2)
        lppls_model.plot_confidence_indicators(res)
        plt.title(f'{ticker} - Confidence Indicators')
        
        # Save the plot
        plt.tight_layout()

        plt.show()

        #plt.savefig(f'{ticker}_lppls_analysis.png')
        #plt.close()
        
        # Return critical information
        return {
            'ticker': ticker,
            'critical_time': tc,
            'm': m,
            'w': w,
            'a': a,
            'b': b,
            'c': c,
            'O': O,
            'D': D
        }
    
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None

def main():
    # Configuration
    START = '2022-01-01'
    END = '2024-12-04'
    
    # List of tickers to analyze
    tickers = ['NQ=F', 'ES=F', 'AAPL', 'GOOGL', 'MSFT']
    
    # Store results
    all_results = []
    
    # Use ProcessPoolExecutor for better multiprocessing
    with ProcessPoolExecutor(max_workers=3) as executor:
        # Submit jobs for each ticker
        future_to_ticker = {executor.submit(process_ticker, ticker, START, END): ticker for ticker in tickers}
        
        # Collect results
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                result = future.result()
                if result:
                    all_results.append(result)
            except Exception as e:
                print(f"Unexpected error for {ticker}: {e}")
    
    # Create a DataFrame of results for easy comparison
    if all_results:
        results_df = pd.DataFrame(all_results)
        print("\nLPPLS Analysis Results:")
        print(results_df)
        
        # Optional: Save results to CSV
        results_df.to_csv('lppls_analysis_results.csv', index=False)
    else:
        print("No results were generated.")

if __name__ == "__main__":
    main()