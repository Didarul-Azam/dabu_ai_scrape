# html_saver.py
import asyncio
from random import randint
from headers_utils import get_headers
from playwright.async_api import async_playwright
import logging
import aiofiles
import json
import os
from gemini import gemini
EXTRACT_PRODUCT_DETAILS_PROMPT = """Analyze the attached HTML file and extract the product title, description, and the best image associated with that product. Follow these instructions:
1. Remove any newline characters and clean the title by removing all special characters to ensure it is readable.
2. Ensure that image links are fully completed and correctly formatted in the returned response. If the link is incomplete, complete it to form a full URL.
3. If the HTML file is invalid (e.g., it contains a CAPTCHA or lacks essential information like the title, description, or image), return an empty dictionary `{{}}`.
4. Thoroughly analyze the HTML content to create a detailed and accurate product description. The description should clearly describe the product but should not exceed 7 to 8 lines.
5. Create a concise and meaningful title for the product. It should be short but descriptive enough to convey the essence of the product.
The output must include all the fields title, product description, and best image in proper JSON format, like this: {{\"title\":\"Product Title\",\"description\":\"Product Description\",\"best_image\":\"https://link_to_best_image\"}}"""



# Initialize logger
logging.basicConfig(level=logging.INFO, filename="logs/app.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def strip_url(url):
    idx = url.find("?")
    if idx != -1:
        url = url[:idx]

    if url.startswith("//www"):
        url = url.replace("//www", "https://www")

    return url
async def save_page_html(url,output_file,retries=3):
    headers_lst = get_headers()

    # Pick a random header
    random_index = randint(0, len(headers_lst) - 1)
    random_header = headers_lst[random_index]

    headers = {
        'User-Agent': random_header.get('user-agent', ''),
        'Sec-Ch-Ua-Platform': random_header.get('sec-ch-ua-platform', ''),
        'Sec-Ch-Ua': random_header.get('sec-ch-ua', '')
    }

    for attempt in range(retries):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(extra_http_headers=headers)

                try:
                    page = await context.new_page()
                    # Use a timeout for page navigation (e.g., 30 seconds)
                    await page.goto(url, timeout=30000)
                    logger.info(f'Visited page {url}')

                    # Scroll down to ensure JS content loads
                    scroll_step = 1000
                    await page.evaluate(f"window.scrollBy(0, {scroll_step})")
                    logger.info(f'Scrolled {scroll_step}px and waiting 1 second...')
                    await page.wait_for_timeout(1000)

                    # Extract page content
                    content = await page.content()

                    # Create directories if necessary
                    current_directory = os.getcwd()
                    subfolder_path = os.path.join(current_directory, 'html_parse')
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)

                    output_file_path = os.path.join(subfolder_path, output_file)

                    # Save HTML content to file
                    async with aiofiles.open(output_file_path, 'w', encoding='utf-8') as f:
                        await f.write(content)

                    logger.info(f"HTML for {url} saved to {output_file_path}")
                    
                finally:
                    # Ensure context is closed after use
                    await context.close()
                    logger.info(f"Browser context closed for {url}")

                # Ensure browser is closed
                await browser.close()
                logger.info(f"Browser closed after saving {output_file_path}")
                return output_file_path

        except Exception as e:
            logger.warning(f"Retry {attempt+1} failed for {url}. Error: {e}")
            if attempt == retries - 1:
                logger.error(f"All retries failed for {url}. Giving up.")
                return None

    return None

    
async def parse_using_ai(link, file_path):
    dt = {"url": link}
    try:
        print('gemini start')
        fi = await asyncio.to_thread(gemini.upload_file, file_path)
        print('gemini uploaded')
        prompt = EXTRACT_PRODUCT_DETAILS_PROMPT
        response = await asyncio.to_thread(gemini.generate_content, prompt, [fi])
        print('gemini reponse')

        js = json.loads(response.text)
        dt.update(js)
        dt["best_image"] = strip_url(dt.get("best_image", ""))
        current_directory = os.getcwd()
        subfolder_path = os.path.join(current_directory, 'html_parse')
        output_file_path = os.path.join(subfolder_path, 'ai_parsed_info.txt')    
        async with aiofiles.open(output_file_path, 'a', encoding='utf-8') as f:
            await f.write(json.dumps({"url": link, 'ai_parse':dt}) + "\n")
            logger.info(f"HTML AI Parse for {link} saved to {output_file_path}")
        return dt
    except Exception as e:
        print(f"Error in parse_using_ai: {str(e)}")
        return dt
if __name__ == "__main__":
    url = input("Enter the URL of the page to save: ")
    output_file = input("Enter the output file name: ")
    html_txt_path = asyncio.run(save_page_html(url,output_file))
    #print(html_txt_path)
    asyncio.run(parse_using_ai(url,html_txt_path))
