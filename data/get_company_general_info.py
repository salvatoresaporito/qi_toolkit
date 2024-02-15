import pandas as pd
import yfinance as yf
import os
from datetime import datetime
from tqdm import tqdm
def read_filtered_symbols(file_path: str, symbol_column: str) -> list:
    """Read and filter symbols from a given NASDAQ or other listed file."""
    df = pd.read_csv(file_path, sep='|')
    df = df[df.ETF == 'N']
    df = df[df['Test Issue'] == 'N']
    print(df.columns)
    df = df[~df.loc[:,symbol_column].str.contains('\$').fillna(False)]
    return df.loc[:,symbol_column].tolist()

def get_links_usa() -> list:
    """Aggregate filtered symbols from NASDAQ and other listed files."""
    nasdaq_symbols = read_filtered_symbols('../dataset/nasdaqlisted.txt', 'Symbol')
    other_symbols = read_filtered_symbols('../dataset/otherlisted.txt', 'ACT Symbol')
    return nasdaq_symbols + other_symbols

def get_company_info_yf(tickers: list,
                        output_dir = '../dataset/general_company_info'):
    """Download and save company information for each ticker symbol."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    for ticker in tqdm(tickers):
        output_path = os.path.join(output_dir, f'{ticker}.csv')
        if os.path.exists(output_path):
            print(f'{ticker} exists')
            continue
        
        ticker_info = yf.Ticker(ticker)
        try:
            info_df = pd.DataFrame.from_dict(ticker_info.info, orient='index').T
            info_df.to_csv(output_path)
            print(ticker)
        except Exception as e:
            print(f'{ticker} FAIL: {e}')

if __name__ == "__main__":
    tickers = get_links_usa()
    get_company_info_yf(tickers)
