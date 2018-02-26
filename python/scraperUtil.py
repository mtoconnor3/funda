# necessary libraries
from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import datetime

# for use in the file naming function
now = datetime.datetime.now()

# Read the source to see if there's bot detection happening. 
def caught_by_bot(page_source):
	soup = BeautifulSoup(page_source, 'html.parser')
	print "checking for bot detection"
	try:
		return soup.find('h1', {'class':'app-error-hero-title'}).text == "We denken dat je een robot bent"
		print "\nbot detection!"
	except:
		return False

# figure out how many pages we need to scrape
def get_pagination(page_source):
	soup = BeautifulSoup(page_source, 'html.parser')
	pagination = soup.find('div', {'class':'pagination-pages'}).find_all('a')
	return int(pagination[-1].text.split()[1])

# Build urls for each page to scrape, using the pagination to construct them
def page_builder(pages, stem):
	pagelist = []
	for i in range(2,pages+1):
		tail = "p%d/" % (i)
		href = stem+tail
		pagelist.append(href)
	return pagelist

# Get the array of listings in the HTML
def get_listings(page_source):
	soup = BeautifulSoup(page_source, 'html.parser')
	listings = soup.find_all('div', {'class':'search-result-content-inner'})
	return listings

# extract data from each idividual listing
def get_listing_address(listing):
	title = listing.find('h3', {'class':'search-result-title'}).text
	title = " ".join(title.split())
	return title

def get_listing_price(listing):
	price = listing.find('span', {'class':'search-result-price'}).text
	return int(price.split()[1].replace(".",""))

def get_listing_sqm(listing):
	sqm = listing.find('ul', {'class': 'search-result-kenmerken'})
	sqm = sqm.find_all('span', {'title': 'Woonoppervlakte'})[0].text
	return int(sqm.split()[0])

def get_listing_parcel(listing):
	parcel = listing.find('ul', {'class': 'search-result-kenmerken'})
	parcel = parcel.find('li').find_all('span')[1].text
	return int(parcel.split()[0])

def get_listing_rooms(listing):
	rooms = listing.find('ul', {'class': 'search-result-kenmerken'})
	rooms = rooms.find_all('li')[1].text
	return int(rooms.split()[0])

def get_listing_href(listing):
	href = listing.find_all('div', {'class':'search-result-header'})[0].find('a')['href']
	return href 

# put all of the above to work for you:
def get_listing_data(listing, verbose = False):
	try: 
		address = get_listing_address(listing)
	except:
		if verbose:
			print "no address found for this listing"
		address = None
	try:
		price = get_listing_price(listing)
	except: 
		if verbose:
			print "no price found for this listing: %s" %address 
		price = None
	try:
		sqm = get_listing_sqm(listing)
	except:
		if verbose:
			print "no sqm found for this listing: %s" %address 
		sqm = None 
	try:
		parcel = get_listing_parcel(listing)
	except:
		if verbose:
			print "no parcel info found for this listing: %s" %address 
		parcel = None
	try: 
		rooms = get_listing_rooms(listing)
	except:
		if verbose:
			print "no rooms data found for this listing: %s" %address 
		rooms = None
	try:
		href = get_listing_href(listing)
	except:
		if verbose:
			print "no href found for this listing: %s" %address 
	return {'href':href, 'address':address, 'price':price, 'sqm':sqm, 'parcel':parcel,'rooms':rooms}

# filename builder
def namefile():
	date = now.strftime("%Y_%m_%d")
	return "funda_scrape_"+str(date)+".csv"
