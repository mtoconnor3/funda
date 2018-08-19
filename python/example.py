from scraperUtil2 import *

funda = "https://www.funda.nl/koop/amsterdam/0-51-woonopp/appartement/"

# Configure selenium to mimic a normal computer browser

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
browser = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=opts)
browser.set_page_load_timeout(30)

# Get the first page of the search, and wait for the javascript to render

browser.get('http://www.funda.nl')
browser.get(funda)  
sleep(5)
sr = search_results_page(browser)

# Past bot detection? get the pagination

sr.get_pagination()
links = sr.pagelist

# create the array with data in it

listingData = [search_result(listing).listing_data for listing in sr.listings]
# loop over remaining links

for page in links:
	browser.get(page) 
	sr = search_results_page(browser)
	for listing in sr.listings:	
		try:
			listingData.append(search_result(listing).listing_data)
		except: 
			print "invalid record"
			pass

listingLinks = [d['href'] for d in listingData]
listingAddresses = list(df['address'])

# this bit will take a while, so buckle up

listingDetails = []
for i in range(0,len(listingLinks)):
	
	print "%s getting %s" %(i, listingLinks[i])
	try:
		browser.get(listingLinks[i])
		l = listing_page(browser)
		l.data['address']= listingAddresses[i]
		listingDetails.append(l.data)
	except:
		print 'Exception - moving on to the next listing'
		pass
	# not trying to be a jerk here, ya know. 
	sleep(1.5)

data2 = df(listingDetails)
data2.to_csv(namefile(), sep = ',', encoding = 'utf-16', index = False)

