import os
import asyncio
import yt_dlp
from random import randint
import time
from headers_utils import get_headers
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO, filename="logs/app.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def download_song(song_title, artist, output_file, geo_location=None,max_retries = 3,retry_delay=5):
    '''
    song_title: title of the song to be downloaded
    artist: name of the artist
    output_file: output_file name. It creates that file within 'downloaded song' folder
    geo_bypass_country:
                       Two-letter ISO 3166-2 country code that will be used for
                       explicit geographic restriction bypassing via faking
                       X-Forwarded-For HTTP header
    max_retries: number of maximum retires before the download fails(default 3)
    retry_delay: waiting interval between subsequent retries(deafault 5 seconds)                   
    '''
    headers_lst = get_headers()
    if not headers_lst:
        logger.error("No headers available. Cannot proceed with download.")
        return

    query = f"{song_title} {artist} audio"
    os.makedirs('downloaded_song',exist_ok=True)
    output_file = os.path.join('downloaded_song',output_file)
    output_dir = os.path.dirname(output_file)

    # Check if the output directory exists, if not create it
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        except OSError as e:
            logger.error(f"Error creating directory {output_dir}: {e}")
            return
    for attempt in range(1, max_retries + 1):
        # Pick a random header
        if headers_lst:
            random_index = randint(0, len(headers_lst) - 1)
            random_header = headers_lst[random_index]
        else:
            random_header = {}    
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_file + '.%(ext)s',  # Correct extension
            'http_headers': {
                'User-Agent': random_header.get('user-agent', ''),
                'Sec-Ch-Ua-Platform': random_header.get('sec-ch-ua-platform', ''),
                'Sec-Ch-Ua': random_header.get('sec-ch-ua', ''),
            }

        }

        #If geo_location is provided, add the geo_bypass_country options
        if geo_location:
            ydl_opts['geo_bypass_country'] = geo_location

        try:
            logger.info(f"Starting download for: {song_title} by {artist}")
            await asyncio.to_thread(lambda: yt_dlp.YoutubeDL(ydl_opts).download([f"ytsearch1:{query}"]))
            logger.info(f"Download successful on attempt {attempt}")
            break
        except Exception as e:
            logger.error(f"Error downloading song: {e}")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                logger.error(f"Failed to download song after {max_retries} attempts")

if __name__ == "__main__":
    song_title = input("Enter song title: ")
    artist = input("Enter artist name: ")
    output_file = input("Enter output file name (with path, without extension): ")
    #geo_location = input("Enter geo-location (ISO country code or CIDR IP block) or leave blank: ")

    asyncio.run(download_song(song_title, artist, output_file))
