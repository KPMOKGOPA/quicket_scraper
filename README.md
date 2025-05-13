# Quicket Event Scraper

This tool scrapes event listings from [Quicket](https://www.quicket.co.za/events/) using Selenium and BeautifulSoup.

## Features
- Scrapes title, venue, date, and time of events
- Command-line options for headless browsing and page count

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

or you may use pip 
``` bash
pip show beautifulsoup4
pip show selenium
```
## usage

####  Run the scraper:

```bash
python run_scraper.py
```

By default, this scrapes **10 pages** in **headless mode**.

#### Optional arguments:

| Argument     | Type | Default | Description                             |
| ------------ | ---- | ------- | --------------------------------------- |
| `--pages`    | int  | `10`    | Number of event listing pages to scrape |
| `--headless` | bool | `True`  | Run browser in headless (no-GUI) mode   |


* Scrape 5 pages with a visible browser:

  ```bash
  python run_scraper.py --pages 5 --headless False
  ```

* Scrape 20 pages in headless mode:

  ```bash
  python run_scraper.py --pages 20
  ```




