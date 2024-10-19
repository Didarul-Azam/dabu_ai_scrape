# Web Scraping and Song Downloader Project

This project consists of two main components: a **web scraper** that uses `playwright` to save and parse HTML content, and a **song downloader** that leverages `yt-dlp` for downloading songs. It demonstrates efficient asynchronous execution, logging, and error handling while using popular Python libraries for web scraping and media downloading.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Folder Structure](#folder-structure)
- [Libraries and Dependencies](#libraries-and-dependencies)
- [Usage Instructions](#usage-instructions)
  - [Web Scraping (HTML Saver)](#web-scraping-html-saver)
  - [Song Downloader](#song-downloader)
- [Logging](#logging)
- [Error Handling](#error-handling)

---

## Project Overview

1. **Web Scraping**: 
   The web scraping component extracts HTML content from web pages, even JavaScript-rendered pages, and saves them locally in a structured format.
   
2. **Song Downloader**: 
   The song downloader uses `yt-dlp` to download songs by title and artist from YouTube or similar platforms. It supports downloading songs multiple times in parallel to test the load capability.

## Requirements

To run this project, you will need the following libraries:

- `yt-dlp==2024.9.27`
- `playwright==1.47.0`
- `aiofiles`
- `requests`
- `asyncio`
- `logging`
- `random`

Ensure all dependencies are installed by following the installation instructions below.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Install browser dependencies for Playwright:

    ```bash
    pip install playwright
    ```

---

## Folder Structure

    The folder structure for this project looks like this:
    project/
    ├── logs/                       (Directory for logging information)
    │   └── app.log                 (Log file containing application events)
    ├── headers_cache.json          (JSON file for caching fake headers)
    ├── html_parse/                     (Directory for storing parsed HTML files)
    │   ├── new_of1.txt,...new_of8.txt  (txt files storing parsed HTML data)
    │   └── ai_parsed_info.txt          (txt file containing AI-parsed information from HTML)
    ├── downloaded_song/                (Directory for parallel processing of songs download)
    |   └──  11am.mp3, ..., Unforgiven 2.mp3  
    │   └── Bilionera_1, Bilionera_2, ..., Bilionera_50  (Files containing 50 Bilionera songs for demonstration)
    ├── yt_downloader.py            (Python script for downloading youtube songs)
    ├── html_saver.py               (Python script for saving HTML data)
    ├── requirements.txt            (Text file specifying project dependencies)
    ├── test.ipynb                  (Providing test for the functions)
    └── README.md                   (This file - project documentation)


---

## Libraries and Dependencies

The core libraries used in this project are:

- **`yt-dlp`**: A powerful media downloader for YouTube and other platforms.
- **`playwright`**: A modern library to automate and scrape web pages, including JavaScript-rendered content.
- **`aiofiles`**: An asynchronous file library to handle file operations without blocking the event loop.
- **`requests`**: A simple library to send HTTP requests.
- **`logging`**: Python's built-in logging library for robust logging and error tracking.
- **`random`**: For selecting random headers during web scraping.

## Usage Instructions

### Web Scraping (HTML Saver)

1. **Save the HTML content of a webpage:**

   The function `save_page_html(url, output_file)` takes a URL and a desired output file name and saves the entire HTML of the page to the output file. It handles JavaScript-rendered content by scrolling and waiting for content to load. It returns the output_file path for convenience to be further processed by ai agent. It has optional `retries` argument set to 3 for 3 retries for each link.

   Example usage:
   
   ```python
   asyncio.run(save_page_html("https://example.com", "output.html",4))#using 4 retries
2. **Parse the HTML using AI:**
    After the HTML is saved, the `parse_using_ai()` function can be used to analyze and extract structured data from the saved HTML.

    Example usage:
   
   ```python
   asyncio.run(parse_using_ai("https://example.com", "output.html")) #second argument can be retrieved from return of save_page_html
### Song Downloader(yt_downloader)
1. **Download a song by title and artist:**
    The `download_song(song_title, artist, output_file)` function downloads a song based on the provided title and artist.

    Example usage:
   
   ```python
   asyncio.run(download_song("Song Title", "Artist", "output_file"))
### test.ipynb:
   - **`test.ipynb`** file demonstrates different asynchronous use cases for the project
## Logging:
This project implements robust logging using Python's `logging` library. Logs are stored in the `logs/app.log` file at the `INFO` level, which captures important events, warnings, and errors.   
## Error Handling:
- **Web Scraping:** If the web scraping operation fails (e.g., page not loading), an error message is logged and returned with retries number.
- **Song Downloader:** If a song cannot be found or downloaded, an appropriate error message is logged.
