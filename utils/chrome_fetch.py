#!/Users/pedram/venv3/bin/python
# https://chat.openai.com/share/503bbe58-1bed-41c6-82ea-6f4837478d5f

"""
CLI tool and library for fetching content via Chrome driven by Selenium. Has some tricks up its sleeve to evade
mechanized browser detection.

Pedram Amini
https://pedramamini.com

Requirements:
    pip install selenium
    pip install webdriver_manager

Usage:
    usage: chrome_fetch.py [-h] [--echourl] [--sleep SLEEP] [--headless] [--debug] [--referrer [URL]] [--human] [--adblock] [--bypass] [--stats] url

    Fetch the inner text of a webpage.

    positional arguments:
      url               URL of the webpage to fetch

    options:
      -h, --help        show this help message and exit
      --echourl         Echo the URL we are fetching to stderr.
      --sleep SLEEP     Time to wait in-between operations
      --headless        Run in headless mode.
      --debug           Enable debug mode.
      --referrer [URL]  Referrer URL to start from (default: https://www.google.com).
      --human           Mimick human behavior with mouse.
      --adblock         Install uBlock Origin extension.
      --bypass          Install Bypass Paywalls extension.
      --stats           Produce word count and estimated reading time.
"""

import os
import sys
import time
import random
import hashlib
import logging
import argparse
import urllib.request
import urllib.parse

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
UBLOCK_ORIGIN = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=84.0&x=id%3Dcjpalhdlnbpafiamejdnhcphjbkeiagm%26installsource%3Dondemand%26uc"
PATH_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PATH_UBLOCK_ORIGIN = os.path.join(PATH_SCRIPT, 'ublock_origin.crx')
PATH_BYPASS_PAYWALL = '/Users/pedram/Utils/bypass-paywalls-chrome-master'

########################################################################################################################
def text_analysis (text):
    # Calculate word count
    word_count = len(text.split())

    # Estimate reading time
    # Average reading speed is approximately 200 words per minute
    reading_speed_wpm = 200
    reading_time_minutes = word_count / reading_speed_wpm

    # Format the reading time to display it in minutes and seconds
    reading_time_minutes_int = int(reading_time_minutes)
    reading_time_seconds = int((reading_time_minutes - reading_time_minutes_int) * 60)

    # Create the result string
    result = f"Word count: {word_count}, Estimated reading time: {reading_time_minutes_int} minute(s) and {reading_time_seconds} second(s)"

    return result


########################################################################################################################
def remove_utm_params (url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)

    # Parse the query string parameters and filter out UTM parameters
    query_params = urllib.parse.parse_qs(parsed_url.query)
    filtered_params = {k: v for k, v in query_params.items() if not k.startswith('utm_')}

    # Reconstruct the query string without UTM parameters
    query_string = '&'.join(f'{k}={v[0]}' for k, v in filtered_params.items())

    # Reconstruct the URL without UTM parameters
    cleaned_url = urllib.parse.urlunparse(parsed_url._replace(query=query_string))

    # add in https:// by default.
    if not cleaned_url.startswith("http"):
        cleaned_url = "https://" + cleaned_url

    return cleaned_url


########################################################################################################################
def chrome_fetch (url, sleep_time=0.33, headless=False, debug=False, referrer=None, human=False, adblock=False, bypass_paywalls=False):
    """
    Navigates to a specified URL in a Chrome browser session, optionally mimicking human behavior, and returns the text content of the page.

    Args:
        url (str): The target URL from which to fetch the content.
        sleep_time (float, optional): The duration in seconds to pause between actions,
                                      helping to mimic human behavior or allow page elements to load (default is 0.33 seconds).
        headless (bool, optional): If set to True, runs the Chrome browser in headless mode
                                   without a GUI (default is False).
        debug (bool, optional): If set to True, enables verbose logging to aid in debugging
                                (default is False).
        referrer (str, optional): A URL to visit before navigating to the target URL,
                                  simulating a user journey from one page to another (default is None, meaning no referrer is used).
        human (bool, optional): If set to True, simulates human-like browsing behavior such as
                                random scrolling and variable timing between actions (default is False).
        adblock (bool, optional): If set to True, installs uBlock Origin prior to fetching (default is False).
        bypass_paywalls (bool, optional): If set to True, installs Bypass Paywalls prior to fetching (default is False).
    Returns:
        str: The text content of the target webpage after it has been fully loaded,
             and after performing any additional simulated human interactions if enabled.

    This function initializes a Chrome browser session, optionally in headless mode, and navigates first to a referrer URL,
    then to the target URL. If human-like behavior is enabled, it simulates human actions like scrolling and random delays to
    make the automation less detectable to anti-bot mechanisms. It waits for the page to load and scrolls to ensure dynamic content
    is loaded, then extracts and returns the text content of the page.
    """

    logger = logging.getLogger()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stderr_handler.setFormatter(formatter)
        logger.addHandler(stderr_handler)
        logger.debug("Debug mode enabled")

    # Set up Chrome options
    chrome_options = Options()

    # enable adblocking.
    if adblock:
        # NOTE: this isn't working, i downlaoded it manually.
        if not os.path.exists(PATH_UBLOCK_ORIGIN):
            logger.debug(f"Downloading uBlock Origin to {PATH_UBLOCK_ORIGIN}")
            urllib.request.urlretrieve(UBLOCK_ORIGIN, PATH_UBLOCK_ORIGIN)

        if os.path.exists(PATH_UBLOCK_ORIGIN):
            logger.debug("Enabling Extension: uBlock Origin")
            chrome_options.add_extension(PATH_UBLOCK_ORIGIN)

    # enable paywall bypassing.
    if bypass_paywalls and os.path.exists(PATH_BYPASS_PAYWALL):
        logger.debug("Enabling Extension: Bypass Paywall")
        chrome_options.add_argument(f'--load-extension={PATH_BYPASS_PAYWALL}')

    # Hide from detection
    chrome_options.add_argument(USER_AGENT)
    chrome_options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")

    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        logger.debug("Headless mode enabled")

    logger.debug("Initializing ChromeDriver")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Hide from detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # Navigate to referrer URL
        if referrer:
            if debug:
                logger.debug(f"Starting at referrer: {referrer}")
            driver.get(referrer)
            if debug:
                logger.debug("Referrer page loaded")

        # Navigate to the target URL
        if debug:
            logger.debug(f"Navigating to {url}")
        driver.get(url)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        if debug:
            logger.debug("Page initially loaded")

        # Human-like behavior on the target site
        if human:
            logger.debug("Human-like behavior enabled")
            actions = ActionChains(driver)

            # Simulate human-like scrolling and content checking
            for _ in range(random.randint(5, 10)):
                scroll_length = random.randint(1000, 1500)
                actions.scroll_by_amount(0, scroll_length).perform()
                time.sleep(random.uniform(0.5, 2))

                if debug:
                    logger.debug(f"Human scrolling: {scroll_length}")

            if debug:
                logger.debug("Human-like scrolling completed")

        # Regular behavior
        last_height = driver.execute_script("return document.body.scrollHeight")

        for _ in range(10):  # Limit the number of scrolls
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(0.1, sleep_time))
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height <= last_height:
                 break

            last_height = new_height

            if debug:
                logger.debug(f"Scrolled to new height: {last_height}")

        old_content = ""
        new_content = driver.find_element(By.TAG_NAME, "body").text

        for _ in range(3):  # Limit the number of content checks
            if hashlib.md5(old_content.encode()).digest() == hashlib.md5(new_content.encode()).digest():
                break
            time.sleep(random.uniform(0.1, sleep_time))
            old_content = new_content
            new_content = driver.find_element(By.TAG_NAME, "body").text
            if debug:
                logger.debug("Content checked")

        return new_content

    finally:
        if debug:
            logger.debug("Quitting driver")

        driver.quit()


########################################################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch the inner text of a webpage.")
    parser.add_argument("url", help="URL of the webpage to fetch")
    parser.add_argument("--echourl", action='store_true', help="Echo the URL we are fetching to stderr.")
    parser.add_argument("--echourlstdout", action='store_true', help="Echo the URL we are fetching to stderr.")
    parser.add_argument("--sleep", type=float, default=0.33, help="Time to wait in-between operations")
    parser.add_argument("--headless", action='store_true', help="Run in headless mode.")
    parser.add_argument("--debug", action='store_true', help="Enable debug mode.")
    parser.add_argument("--referrer", nargs='?', default=None, const="https://www.google.com", help="Referrer URL to start from (default: https://www.google.com).", metavar='URL')
    parser.add_argument("--human", action='store_true', help="Mimick human behavior with mouse.")
    parser.add_argument("--adblock", action='store_true', help="Install uBlock Origin extension.")
    parser.add_argument("--bypass", action='store_true', help="Install Bypass Paywalls extension.")
    parser.add_argument("--stats", action='store_true', help="Produce word count and estimated reading time.")

    args = parser.parse_args()
    url  = remove_utm_params(args.url)

    content = chrome_fetch(url, args.sleep, args.headless, args.debug, args.referrer, args.human, args.adblock, args.bypass)

    if args.echourl:
        sys.stderr.write(url + "\n")

    if args.echourlstdout:
        sys.stdout.write(url + "\n")

    if args.stats:
        sys.stderr.write(text_analysis(content) + "\n")

    print(content)
