import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append('..')
from utils.ftp_downloader import download_ftp_file
import shutil
def download_and_process_files():
    # Define today's date in the specified format
    today = datetime.today().strftime('%Y_%m_%d')

    # FTP details
    ftp_host = 'ftp.nasdaqtrader.com'
    nasdaq_ftp_path = '/symboldirectory/nasdaqlisted.txt'
    other_ftp_path = '/symboldirectory/otherlisted.txt'
    dataset_dir = '../dataset'  # Assuming the dataset directory is at the root of your project

    # Ensure the dataset directory exists
    os.makedirs(dataset_dir, exist_ok=True)

    # Download files
    nasdaq_local_path = os.path.join(dataset_dir, f'nasdaqlisted_{today}.txt')
    other_local_path = os.path.join(dataset_dir, f'otherlisted_{today}.txt')
    download_ftp_file(ftp_host, nasdaq_ftp_path, nasdaq_local_path)
    download_ftp_file(ftp_host, other_ftp_path, other_local_path)
    shutil.copyfile(os.path.join(dataset_dir, f'nasdaqlisted_{today}.txt'),os.path.join(dataset_dir, f'nasdaqlisted.txt'))
    shutil.copyfile(os.path.join(dataset_dir, f'otherlisted_{today}.txt'),os.path.join(dataset_dir, f'otherlisted.txt'))
    # Read the downloaded files into DataFrames
    df_nasdaq = pd.read_csv(nasdaq_local_path, sep='|')
    df_other = pd.read_csv(other_local_path, sep='|')

    return df_nasdaq, df_other

if __name__ == "__main__":
    df_nasdaq, df_other = download_and_process_files()
    print(df_nasdaq.head())
    print(df_other.head())
