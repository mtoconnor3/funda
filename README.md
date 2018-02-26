# Funda Scraper
A generic set of scraper utils for pulling down listing data from funda.nl

## Prerequisites:

* In order for this to work, you will need selenium installed on your machine. You can install with _pip_ or your preferred python installer utility. 
* You will also need the latest version of the browser driver you prefer to use. I prefer chrome, so I use chromedriver found [HERE](https://sites.google.com/a/chromium.org/chromedriver/).
* BeautifulSoup4 - Install using pip, or your favorite installer

## How it works
1. The provided link is loaded
	- The script checks for bot detection
		- If bot detection is enabled, the script waits for a human to solve the captcha
	- Once the page is loaded properly, the pagination and link builder are run
	- All the listings are scraped and recorded to an array
2. For each link in the array of constructed links:
	- Load page
	- Check for bot detection
	- Scrape the page once bot detection is defeated (if necessary)
	- Record result to the listings array
3. Once all links are recorded:
	- Close browser session
	- Write listings data to a CSV file using pandas, with filename = today's date. 