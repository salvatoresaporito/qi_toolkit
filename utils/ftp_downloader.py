import ftplib
from typing import Optional

def download_ftp_file(ftp_host: str, ftp_path: str, local_filename: str, username: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Downloads a file from an FTP server to a local file.

    This function connects to an FTP server at the specified host, logs in using the provided credentials (if any),
    and downloads a file from the given path on the server to a local file.

    Parameters:
    - ftp_host (str): The hostname or IP address of the FTP server.
    - ftp_path (str): The path to the file on the FTP server that needs to be downloaded.
    - local_filename (str): The local path where the file will be saved.
    - username (Optional[str]): The username for FTP server login. If not provided, anonymous login is attempted.
    - password (Optional[str]): The password for FTP server login. Required if a username is provided.

    Returns:
    - None

    Raises:
    - Various ftplib exceptions on errors related to FTP operations.
    - IOError or similar exceptions if there are issues writing the file locally.
    """
    with ftplib.FTP(ftp_host) as ftp:
        # Login using provided credentials, or attempt anonymous login if none are provided
        if username and password:
            ftp.login(user=username, passwd=password)
        else:
            ftp.login()  # Attempt anonymous login

        # Open local file in write-binary mode and download file from FTP
        with open(local_filename, 'wb') as local_file:
            ftp.retrbinary(f'RETR {ftp_path}', local_file.write)
