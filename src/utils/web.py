# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import logging
import urllib.request

def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        urllib.request.urlretrieve(url, destination)
        return True
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return False
