import csv
import time
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

BASE_URL = "https://www.quicket.co.za/events/"

OUTPUT_CSV = "quicket_events.csv"
NUM_PAGES = 10
DELAY_SECONDS = 2  

def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 10)
        accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_btn.click()
        logging.info("Accepted cookies.")
        time.sleep(1)  # Brief delay to let it settle
    except TimeoutException:
        logging.warning("Cookie banner not found or already handled.")

def init_driver(headless=False):
    options = Options()
    options.headless = headless
    return webdriver.Chrome(options=options)

# BeautifulSoup 
def parse_events(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    event_list = []

    containers = soup.find_all('li', class_='l-event-item ng-star-inserted')
    
    for container in containers:
        try:
            title = container.find('div', class_='l-hit').get_text(strip=True)
        except AttributeError:
            title = None

        try:
            venue = container.find('div', class_='l-hit-venue').get_text(strip=True)
        except AttributeError:
            venue = None

        try:
            date_time = container.find_all('div', class_='l-date')
            date = date_time[0].get_text(strip=True) if len(date_time) > 0 else None
            time = date_time[1].get_text(strip=True) if len(date_time) > 1 else None
        except Exception:
            date, time = None, None

        event_list.append({
            'Title': title,
            'Venue': venue,
            'Date': date,
            'Time': time
        })

    return event_list


#  CSV
def save_to_csv(data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Title", "Venue", "Date", "Time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def scrape_quicket(num_pages=10, headless=False):
    logging.info("Starting Quicket scraper...")

    driver = init_driver(headless=headless)
    driver.get(BASE_URL)
    accept_cookies(driver)
    all_events = []

    try:
        for page in range(num_pages):
            logging.info(f"Scraping page {page + 1}...")
            time.sleep(DELAY_SECONDS)
            all_events.extend(parse_events(driver.page_source))

            try:
                wait = WebDriverWait(driver, 5)
                next_icon = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fa-angle-right")))
                next_button = next_icon.find_element(By.XPATH, "./..")
                driver.execute_script("arguments[0].click();", next_button)
            except (NoSuchElementException, TimeoutException):
                logging.warning("No more pages found or next button is missing.")
                break
            except Exception as e:
                logging.warning(f"Could not click next: {e}")
                break

        save_to_csv(all_events, OUTPUT_CSV)
        logging.info(f"Scraped {len(all_events)} events. Data saved to {OUTPUT_CSV}")

    except Exception as e:
        logging.error(f"Error occurred: {e}")

    finally:
        driver.quit()

