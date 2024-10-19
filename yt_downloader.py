import os
import asyncio
import yt_dlp
from random import randint
from headers_utils import get_headers
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO, filename="logs/app.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def download_song(song_title, artist, output_file, geo_location=None):
    headers_lst = get_headers()
    if not headers_lst:
        logger.error("No headers available. Cannot proceed with download.")
        return

    # Pick a random header
    random_index = randint(0, len(headers_lst) - 1)
    random_header = headers_lst[random_index]

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

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_file + '.%(ext)s',  # Correct extension
        'add-headers': [
            f"User-Agent:{random_header.get('user-agent', '')}",
            f"Sec-Ch-Ua-Platform:{random_header.get('sec-ch-ua-platform', '')}",
            f"Sec-Ch-Ua:{random_header.get('sec-ch-ua', '')}",
        ]
    }

    #If geo_location is provided, add the --xff option
    if geo_location:
        ydl_opts['xff'] = geo_location

    try:
        logger.info(f"Starting download for: {song_title} by {artist}")
        await asyncio.to_thread(lambda: yt_dlp.YoutubeDL(ydl_opts).download([f"ytsearch1:{query}"]))
    except Exception as e:
        logger.error(f"Error downloading song: {e}")

if __name__ == "__main__":
    song_title = input("Enter song title: ")
    artist = input("Enter artist name: ")
    output_file = input("Enter output file name (with path, without extension): ")
    #geo_location = input("Enter geo-location (ISO country code or CIDR IP block) or leave blank: ")

    asyncio.run(download_song(song_title, artist, output_file))
