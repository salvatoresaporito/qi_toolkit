import os
import requests
import pandas as pd
from consolidate_company_general_info  import get_all_company_info
# Assuming df_all is defined elsewhere and is a DataFrame containing financial data of companies


def ensure_directory(directory: str):
    """Ensure the given directory exists."""
    os.makedirs(directory, exist_ok=True)

def get_dividend_history(ticker: str):
    """Download and save the dividend history for a given ticker."""
    output_dir = '../datasets/dividends_10y'
    ensure_directory(output_dir)
    
    output_path = os.path.join(output_dir, f'{ticker}.csv')
    if os.path.exists(output_path):
        return

    url = f'https://www.streetinsider.com/dividend_history.php?q={ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}  # Using a more common User-Agent
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            dividend_data = pd.read_html(response.text)[0]
            dividend_data.to_csv(output_path)
        except ValueError as e:
            print(f'Failed to process dividend data for {ticker}: {e}')
    else:
        print(f'Request for {ticker} failed with status code: {response.status_code}')

if __name__ == "__main__":
    df_all = get_all_company_info()
    large_companies = df_all[df_all.marketCap > 1e9][[
        'longName',
        'dividendYield',
        'exDividendDate',
        'pegRatio',
        'symbol',
        'priceToSalesTrailing12Months'
    ]]
    large_companies = large_companies.dropna(subset=['dividendYield'])
    for _, row in large_companies.iterrows():
        get_dividend_history(row['symbol'])
