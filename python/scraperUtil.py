# Necessary libraries
from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import datetime
from pandas import DataFrame as df

# For use in the file naming function
now = datetime.datetime.now()

class search_results_page:
	def __init__(self, browser):
			self.html_source = browser.page_source
			self.soup = BeautifulSoup(self.html_source, 'html.parser')
			self.url = browser.current_url
			while self.caught_by_bot():
				print "\nBot detection!"
				sleep (15)
				self.html_source = browser.page_source
			#self.soup = BeautifulSoup(self.html_source, 'html.parser')
			self.get_listings()
	def caught_by_bot(self):
			print "checking for bot detection on %s" %self.url
			self.soup = BeautifulSoup(self.html_source, 'html.parser')
			try:
				return self.soup.find('h1', {'class':'app-error-hero-title'}).text == "We denken dat je een robot bent"
				print "\nbot detection!"
			except:
				return False
	def get_listings(self):
			self.listings = self.soup.find_all('div', {'class':'search-result-content-inner'})
	def get_pagination(self):
			pagination = self.soup.find('div', {'class':'pagination-pages'}).find_all('a')
			pages = int(pagination[-1].text.split()[1])
			self.pagelist = []
			for i in range(2,pages+1):
				tail = "p%d/" % (i)
				href = self.url+tail
				self.pagelist.append(href)

class search_result:
	def __init__(self, listing):
		self.listing = listing
		self.listing_data = self.get_listing_data()
	def get_listing_address(self):
			title = self.listing.find('h3', {'class':'search-result-title'}).text
			title = " ".join(title.split())
			return title	
	def get_listing_price(self):
			price = self.listing.find('span', {'class':'search-result-price'}).text
			return int(price.split()[1].replace(".",""))	
	def get_listing_sqm(self):
			sqm = self.listing.find('ul', {'class': 'search-result-kenmerken'})
			sqm = sqm.find('span', {'title': 'Woonoppervlakte'}).text
			return int(sqm.split()[0])	
	def get_listing_parcel(self):
			parcel = self.listing.find('ul', {'class': 'search-result-kenmerken'})
			parcel = parcel.find('li').find_all('span')[0].text
			return int(parcel.split()[0])	
	def get_listing_rooms(self):
			rooms = self.listing.find('ul', {'class': 'search-result-kenmerken'})
			rooms = rooms.find_all('li')[1].text
			return int(rooms.split()[0])	
	def get_listing_href(self):
			link = self.listing.find('div', {'class':'search-result-header'}).find('a')['href']
			return link 
	# put all of the above to work for you:	
	def get_listing_data(self, verbose = True):
		try:
			address = self.get_listing_address()
		except:
			print 'missing address'
			address = None
		try:
			price = self.get_listing_price()
		except:
			print 'missing price'
			price = None
		try:
			sqm = self.get_listing_sqm()
		except:
			print 'missing sqm'
			price = None
		try:
			parcel = self.get_listing_parcel()
		except:
			print 'missing parcel'
			price = None
		try:
			rooms = self.get_listing_rooms()
		except:
			print 'missing rooms'
			price = None
		try:
			href = self.get_listing_href()
		except:
			print 'missing href'
			price = None
		return {'href':href, 'address':address, 'price':price, 'sqm':sqm, 'parcel':parcel,'rooms':rooms}

# this is kind of a brute-force method for extracting data, but it works. 
class listing_page:
	def __init__(self, browser):
			self.keys = ["Aangeboden sinds", "Aantal badkamers", "Aantal kamers", "Aantal woonlagen", "Aanvaarding", "Achtertuin", "Badkamervoorzieningen", "Balkon/dakterras", "Bijdrage VvE", "Bouwjaar", "Capaciteit", "Cv-ketel", "Eigendomssituatie", "Energielabel", "Externe bergruimte", "Gebouwgebonden buitenruimte", "Gelegen op", "Inhoud", "Inschrijving KvK", "Isolatie", "Jaarlijkse vergadering", "Laatste vraagprijs", "Lasten", "Ligging", "Ligging tuin", "Looptijd", "Onderhoudsplan", "Oppervlakte", "Opstalverzekering", "Overige inpandige ruimte", "Perceeloppervlakte", "Periodieke bijdrage", "Reservefonds aanwezig", "Schuur/berging", "Soort appartement", "Soort bouw", "Soort dak", "Soort garage", "Soort parkeergelegenheid", "Soort woonhuis", "Specifiek", "Status", "Tuin", "Verkoopdatum", "Verwarming", "Voorlopig energielabel", "Voorzieningen", "Vraagprijs", "Warm water", "Woonoppervlakte"]
			self.soup = BeautifulSoup(browser.page_source, 'html.parser')
			while self.caught_by_bot():
				print "sleeping until captcha is solved"
				sleep (15)
				self.soup = BeautifulSoup(browser.page_source, 'html.parser')
	#def get_listing_data(self):
			headers = [element.text.strip() for element in self.soup.find_all('dt')]
			values = [element.text.strip() for element in self.soup.find_all('dd')]
			self.data = dict(zip(headers,values))
			self.data = {k:self.data[k] for k in self.keys if k in self.data}
	def caught_by_bot(self):
			print "checking for bot detection"
			try:
				return self.soup.find('h1', {'class':'app-error-hero-title'}).text == "We denken dat je een robot bent"
				print "\nbot detection!,"
			except:
				return False

# filename builder
def namefile():
		date = now.strftime("%Y_%m_%d")
		return "funda_scrape_"+str(date)+".csv"
