# Automated QA with Playwright

This project automates QA for web-based reports by scraping and summing numbers from dynamically generated tables.

## What it does

- Scrapes tables from seeds 68-77 on datadash.iitmandi.co.in
- Extracts all numbers from the tables
- Calculates and prints the total sum in GitHub Actions logs

## Running locally

```bash
pip install playwright
playwright install chromium
python scrape_tables.py
```

## GitHub Actions

The workflow runs automatically on push to main/master branch and includes the required email address in the step name.
