import sqlite3
import pandas as pd

def inspect_database():
    """Inspect the database structure to understand the schema"""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Available tables:", tables)
    
    # Get column info for prices table (if it exists)
    try:
        cursor.execute("PRAGMA table_info(prices);")
        columns = cursor.fetchall()
        print("\nColumns in 'prices' table:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")  # column name and type
    except Exception as e:
        print(f"Error inspecting prices table: {e}")
    
    # Show a sample of data
    try:
        cursor.execute("SELECT * FROM prices LIMIT 5;")
        sample = cursor.fetchall()
        print(f"\nSample data from prices table:")
        for row in sample:
            print(row)
    except Exception as e:
        print(f"Error getting sample data: {e}")
    
    conn.close()

def get_price_data(ticker, start, end):
    conn = sqlite3.connect('finance.db')
    
    # First, let's see what columns actually exist
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(prices);")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    print(f"Available columns: {column_names}")
    
    # Common variations of ticker column names
    ticker_column_options = ['ticker', 'symbol', 'stock_ticker', 'stock_symbol', 'Symbol', 'Ticker']
    date_column_options = ['Date', 'date', 'DATE', 'timestamp', 'trading_date']
    
    # Find the correct column names
    ticker_col = None
    date_col = None
    
    for option in ticker_column_options:
        if option in column_names:
            ticker_col = option
            break
    
    for option in date_column_options:
        if option in column_names:
            date_col = option
            break
    
    if not ticker_col:
        conn.close()
        raise ValueError(f"No ticker column found. Available columns: {column_names}")
    
    if not date_col:
        conn.close()
        raise ValueError(f"No date column found. Available columns: {column_names}")
    
    # Build the query with the correct column names
    query = f"""
    SELECT * FROM prices
    WHERE {ticker_col} = ?
    AND "{date_col}" BETWEEN ? AND ?
    ORDER BY "{date_col}"
    """
    
    print(f"Using query: {query}")
    
    try:
        df = pd.read_sql_query(query, conn, params=(ticker, start, end))
        conn.close()
        return df
    except Exception as e:
        conn.close()
        raise e

# Run the inspection first
print("=== Database Inspection ===")
inspect_database()

print("\n=== Attempting to get price data ===")
try:
    df = get_price_data("AAPL", "2022-01-01", "2022-12-31")
    print(f"Successfully retrieved {len(df)} rows")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")

# Alternative: If you know the correct column name, use this simpler version
def get_price_data_fixed(ticker, start, end, ticker_col='symbol', date_col='Date'):
    """
    Fixed version where you specify the correct column names
    
    Parameters:
    ticker: stock ticker symbol
    start: start date
    end: end date
    ticker_col: actual name of the ticker column in your table
    date_col: actual name of the date column in your table
    """
    conn = sqlite3.connect('finance.db')
    query = f"""
    SELECT * FROM prices
    WHERE {ticker_col} = ?
    AND "{date_col}" BETWEEN ? AND ?
    ORDER BY "{date_col}"
    """
    df = pd.read_sql_query(query, conn, params=(ticker, start, end))
    conn.close()
    return df

# Example usage with common column names:
# df = get_price_data_fixed("AAPL", "2022-01-01", "2022-12-31", ticker_col='symbol', date_col='Date')