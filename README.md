# Zillow-Automation
Zillow Web Scraper and Google Sheets Automation - A Python program utilizing Selenium and BeautifulSoup to scrape housing data from Zillow, extract property details, and automate input into a Google Form for real estate analysis.

# Prerequisites
- Python 3.x
- Chrome WebDriver (ensure it matches your Chrome browser version)
- Selenium
- BeautifulSoup
- Google Form URL (for data submission)

# Setup
1. Install the required Python packages using pip: **pip install selenium beautifulsoup4**
2. Download the Chrome WebDriver and specify its path in the `DRIVER_PATH` variable.
3. Set the Zillow URL for the real estate listings in the `URL` variable and the Google Form URL in `GOOGLE_FORM` for data submission.

# Usage
- Ensure you have the correct Google Form URL specified in the GOOGLE_FORM variable within the script.
- Run the payscale.py script to initiate web scraping of real estate data.
- The script will automatically navigate to the specified Zillow URL and collect property information, including prices and addresses.
- The script will then use Google Forms to submit the scraped data to a Google Sheets spreadsheet.
- The automation will continue until all scraped data is successfully submitted to Google Sheets.
- You can review and analyze the organized real estate data in the Google Sheets spreadsheet for your specific purposes.
