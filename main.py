import urllib.parse
import platform
import time
import sys
import os
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import logging
import argparse
import concurrent.futures
import re
import random

def Check_Platform():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() in ['Linux', 'Darwin']:
        os.system('clear')
    else:
        print('Command Not Found')
        exit()

Check_Platform()

banner = '''\033[1;32;40m

█▄░█ █▀▀ █▄▄ █░█ █░░ ▄▀█ █▀▄ █▀█ █▀█ █▄▀
█░▀█ ██▄ █▄█ █▄█ █▄▄ █▀█ █▄▀ █▄█ █▀▄ █░█
========================================
Github:ammeeshaheshan        Version:1.3
========================================

'''

def animated_banner(text, delay=0.008):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

animated_banner(banner)

logging.basicConfig(filename='dorking.log', level=logging.INFO, format='%(asctime)s - %(message)s')

parser = argparse.ArgumentParser(description='Google Dork Search Tool')
parser.add_argument('--dork', help='Dork query', required=True)
parser.add_argument('--pages', type=int, help='Number of pages to fetch', default=1)
parser.add_argument('--filter', help='Filter by domain (e.g. .gov, .edu)', default=None)
parser.add_argument('--file-type', help='Filter by file type (e.g. pdf, doc)', default=None)
parser.add_argument('--delay', type=int, help='Delay between requests (seconds)', default=5)
parser.add_argument('--save', help='Save output to file', action='store_true')
parser.add_argument('--verbose', help='Verbose mode for debugging', action='store_true')
parser.add_argument('--captcha-api', help='API key for CAPTCHA solving service (e.g. 2captcha)', default=None)
parser.add_argument('--threads', type=int, help='Number of threads for parallel requests (min 1, max 10)', default=1, choices=range(1, 11))
parser.add_argument('--show-title', help='Show titles of the search results along with URLs', action='store_true')
parser.add_argument('--output-filter', help='Output URL filter (e.g., php?*=)', default=None)
parser.add_argument('--random-user-agent', help='Use random User-Agent headers from a specified file', default=None)
parser.add_argument('--sql-injection', help='Test for SQL injection vulnerabilities', action='store_true')
args = parser.parse_args()

baseUrl = 'https://www.google.com/search?q={0}'.format(args.dork)
urls = set()

def load_user_agents(file_path):
    try:
        with open(file_path, 'r') as f:
            user_agents = [line.strip() for line in f.readlines() if line.strip()]
            return user_agents
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

if args.random_user_agent:
    user_agents = load_user_agents('ua.txt')

def solve_captcha():
    if args.captcha_api:
        print("Using CAPTCHA solving service.")
        pass

def output_filter(url, pattern):
    regex_pattern = re.escape(pattern).replace('\\*', '.*')
    return bool(re.search(regex_pattern, url))

def fetch_page(page):
    start = page * 10
    search_url = f"{baseUrl}&start={start}"

    if args.verbose:
        print(f"[*] Fetching page {page + 1} from {search_url}")
    
    headers = {'User-Agent': random.choice(user_agents)} if args.random_user_agent else None
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        if "captcha" in response.text.lower():
            print("CAPTCHA detected. Trying to solve it...")
            logging.info("CAPTCHA detected on page {page + 1}")
            solve_captcha()
            return

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/url?q='):
                clean_url = href.split('/url?q=')[1].split('&')[0]
                decoded_url = urllib.parse.unquote(clean_url)

                if args.filter and args.filter.lower() not in decoded_url.lower():
                    continue

                if args.file_type and not decoded_url.lower().endswith(f'.{args.file_type.lower()}'):
                    continue

                if args.output_filter and not output_filter(decoded_url, args.output_filter):
                    continue

                urls.add(decoded_url)

                if args.show_title:
                    title = link.text.strip()
                    print(f"Title: {title}")
                    print(f"URL: {decoded_url}\n")
                else:
                    print(f"URL: {decoded_url}")

        logging.info(f"Fetched page {page + 1} for dork: {args.dork}")

    elif response.status_code == 429:
        print(f"Too many requests. Got status code {response.status_code}. Retrying after a longer delay...")
        logging.warning(f"Status code 429 on page {page + 1}. Applying longer delay.")
        time.sleep(args.delay * 5)

    else:
        print(f"Failed to fetch page {page + 1}. Status code: {response.status_code}")
        logging.error(f"Failed to fetch page {page + 1}. Status code: {response.status_code}")

def check_sql_injection(url):
    sql_payload = "'"
    target_url = url + sql_payload
    headers = {'User-Agent': random.choice(user_agents)} if args.random_user_agent else None

    try:
        response = requests.get(target_url, headers=headers)
        if "SQL syntax" in response.text or "Warning: mysql" in response.text or "You have an error in your SQL syntax" in response.text:
            print(f"\033[1;31;40m[+] Possible SQL injection vulnerability found: {url}")
            logging.info(f"Possible SQL injection vulnerability found: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing SQL injection for {url}: {e}")
        logging.error(f"Error testing SQL injection for {url}: {e}")

with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
    executor.map(fetch_page, range(args.pages))

if urls:
    print("\nExtracted URLs:")
    for url in urls:
        print('\033[1;31;40m'+url)

        if args.sql_injection:
            check_sql_injection(url)

else:
    print("No URLs found.")

if args.save:
    with open('output_urls.txt', 'w') as f:
        for url in urls:
            f.write(url + '\n')
    print('URLs saved to output_urls.txt')
    logging.info("URLs saved to output_urls.txt")