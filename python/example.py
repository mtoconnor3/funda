# import the utilities from the other file
from scraperUtil import *

# The initial funda search we want to scrape in its entirety
funda = "https://www.funda.nl/koop/gemeente-amsterdam/verkocht/300000-700000/sorteer-afmelddatum-af/"

# Configure selenium to mimic a normal computer browser
opts = Options()
opts.add_argument("user-agent=Mozillaaaaa/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)")
browser = webdriver.Chrome(chrome_options=opts)
browser.manage().timeouts().pageLoadTimeout(15, TimeUnit.SECONDS)

# Get the first page of the search, and wait for the javascript to render
browser.get(funda)  
sleep(5)

# Extract the html from the rendered page and check for bot detection
html_source = browser.page_source  
while caught_by_bot(html_source):
	print "sleeping till the captcha is solved"
	sleep(15)
	html_source = browser.page_source

# Once the bot detection has been defeated, build pagination and links
pageNumber = get_pagination(html_source)
page_links = page_builder(pageNumber, funda)

# Extract the first page of listings
listings = []
for listing in get_listings(html_source):
	listings.append(get_listing_data(listing))

# loop over every subsequent page, and extract the listing data
for page in page_links[10:]:
	print "getting page %s" % page
	browser.get(page)  
	sleep(1)
	html_source = browser.page_source  
	# Check for bot detection at each page load
	while caught_by_bot(html_source):
		print "\nSleeping till the captcha is solved.\n"
		sleep(5)
		html_source = browser.page_source
	# Extract listing data from the rendered html
	for listing in get_listings(html_source):
		listings.append(get_listing_data(listing))


# close the browser and
df = pandas.DataFrame(listings)
listings = list(df['href'])
listingDetails = []
for page in listings[:20]:
	browser.get(page)
	l = listing_page(browser)
	listingDetails.append(l.data)
	# not trying to be a jerk here, ya know. 
	sleep(1.5)

browser.quit()

# Save the file
destination_directory = "~/Documents/"
filename = destination_directory+namefile()
df.to_csv(filename, sep = ",", encoding = 'utf-16', index = False)
df.to_csv("details"+filename, sep = ",", encoding = 'utf-16', index = False)

