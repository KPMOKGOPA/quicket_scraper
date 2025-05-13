# run_scraper.py
import argparse
from scrapper import scrape_quicket

def str2bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(description="Run Quicket Event Scraper.")
    parser.add_argument('--pages', type=int, default=10, help='Number of pages to scrape (default: 10)')
    parser.add_argument('--headless', type=str2bool, nargs='?', const=True, default=True,
                        help='Run browser in headless mode (default: True)')

    args = parser.parse_args()

    scrape_quicket(num_pages=args.pages, headless=args.headless)

if __name__ == '__main__':
    main()
