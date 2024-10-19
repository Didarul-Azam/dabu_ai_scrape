import requests
import json
import os
from datetime import datetime, timedelta
import logging

# Ensure the logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    # Configure the logger
    log_file = os.path.join(log_dir, 'app.log')
# Initialize logger
logging.basicConfig(level=logging.INFO, filename="logs/app.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuration constants
SCRAPEOPS_API = "af1bb255-8334-4678-a631-77a29cff9afb"
SCRAPEOPS_HEADERS_ENDPOINT = "https://headers.scrapeops.io/v1/browser-headers"
SCRAPEOPS_HEADERS_NUM = 50  # Number of headers to request

# Path to store the headers and timestamp
HEADERS_FILE_PATH = 'headers_cache.json'

def fetch_headers_from_api():
    payload = {
        'api_key': SCRAPEOPS_API,
        'num_results': SCRAPEOPS_HEADERS_NUM
    }
    try:
        response = requests.get(SCRAPEOPS_HEADERS_ENDPOINT, params=payload)
        response.raise_for_status()
        json_response = response.json()
        headers_lst = json_response.get('result', [])
        logger.info(f"Fetched headers successfully on {datetime.now().isoformat()}")
        return headers_lst
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching headers: {e}")
        return []

def save_headers_to_file(headers_lst):
    data = {
        'headers': headers_lst,
        'timestamp': datetime.now().isoformat()  # Save current time
    }
    with open(HEADERS_FILE_PATH, 'w') as f:
        json.dump(data, f)
        logger.info(f'saved headers to file on {datetime.now().isoformat()}')
def load_headers_from_file():
    if os.path.exists(HEADERS_FILE_PATH):
        with open(HEADERS_FILE_PATH, 'r') as f:
            data = json.load(f)
            headers_lst = data.get('headers', [])
            timestamp = data.get('timestamp', None)
            if headers_lst and timestamp:
                return headers_lst, datetime.fromisoformat(timestamp)
    return [], None

def get_headers():
    headers_lst, last_fetched = load_headers_from_file()

    # Check if we need to fetch new headers (older than 12 hours)
    if not headers_lst or (last_fetched and datetime.now() - last_fetched > timedelta(hours=12)):
        headers_lst = fetch_headers_from_api()
        if headers_lst:
            save_headers_to_file(headers_lst)

    return headers_lst
