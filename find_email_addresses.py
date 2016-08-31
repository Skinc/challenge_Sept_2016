import sys
# import urllib2
from bs4 import BeautifulSoup
import re
from urlparse import urlparse
from email.utils import parseaddr
import requests

class Email_Finder():
	def __init__(self, debug = False, find_all_internal_links = False):
		# Turns on/off debug mode to print what is happening
		self.debug = debug
		# self.find_all_internal_links determines whether the Email Finder should find internal links on all internal pages, or only the homepage
		# web.mit.edu, for example, is very deep with when searching all internal links
		self.find_all_internal_links = find_all_internal_links
		if find_all_internal_links:
			self.debug_print("Finding all internal links")
		else:
			self.debug_print("Finding internal links only from homepage")	
		self.reset()
	
	def reset(self):
		""" Resets the email Email_Finder
		"""

		self.debug_print("Resetting Email_Finder")
		self.all_pages = []
		self.to_do_pages = []
		self.all_emails = []


	def process_domain(self, domain):
		""" Processes all the internal links in a domain to find all the email addresses
		"""
		
		self.reset()
		self.domain = domain
		# setup the regex used to see if urls are internal
		self.domain_regex = "//" + self.domain + "|www."+ self.domain
		
		self.debug_print("Processing domain: " + domain)
		#Process the homepage
		self.process_page("", True)
	
		# Goes through all the pages found and processes them
		while (len(self.to_do_pages) > 0):
			page = self.to_do_pages.pop()
			self.process_page(page, False)
		self.print_emails()

	def build_url(self, path):
		""" Takes a path and generates the URL. 
		"""

		# If the path is accidently absolute, get the relative path
		if self.domain in path:
			path = path.split(self.domain)[1]
		return "http://www." + self.domain + path
		
	def process_page(self, page, is_domain):
		""" Process a page to find all the links and emails on it
		"""

		url = self.build_url(page)
		self.debug_print("Processing: " + url)
		# opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
  #   	request = opener.open(url)
  #   	print request.url
		response =  requests.get(url)
		if ("text/html" in response.headers["content-type"]) and (re.search(self.domain_regex, response.url)):
			
			self.page_soup = BeautifulSoup(response.content, "html.parser")
			
			if self.find_all_internal_links or is_domain:
				self.process_links_from_page()
			
			self.process_emails_from_page()

	def process_links_from_page(self):
		""" Search through links on a page to find internal links """


		for link in self.page_soup.find_all( href = re.compile(self.domain_regex)):
			self.add_page(link["href"])
		
		for link in self.page_soup.find_all("a", href=re.compile("^/")):
			if link["href"][0:2] != "//":
				self.add_page(link["href"])
		
	def process_emails_from_page(self):
		""" Search through html of a page to find emails 
			Searches in two ways:
			1. Looks for mailto in the href
			2. Looks for email addresses in the text

			While this will often find duplicates, there are cases where addresses aren't written with a mailto
			or the text says somethig besides the email address ("Email Us" for example).
		"""

		# Finds all mailtos: in the href of the page.   	
		for mailto in self.page_soup.find_all( href = re.compile("^mailto:")):
			# parse out the address from the mailto and remove any parameters 
			parsed_address = parseaddr(mailto["href"])[1].split("?")[0]
			self.add_email(parsed_address)
			

		# The first for loop will find the complete text that as a match for an email address
		# The second for loop will find all email addresses within that complete text
		# For example, "Contact us at abc@def.com or ghi@def.com" would be the re_match
		# We would then search it find all the email addresses found within
		for re_match in self.page_soup.find_all( text = re.compile("[^ @\s]+@+[^@\s]+\.[^@\s]+")):
			for email in re.findall("[^ @\s]+@+[^@\s]+\.[^@\s]+", re_match):
				self.add_email(email)


	def add_page(self, page):
		""" Checks if a page's path is already in all_pages. If it isn't adds it to all_pages and to_do_pages
		"""
		
		#gets the path, which is the third element returned by urlparse
		path = urlparse(page)[2]
		if path not in self.all_pages:
			self.debug_print("Adding found path: " + path)
			self.all_pages.append(path)
			self.to_do_pages.append(path)
		
	def add_email(self, email):
		""" Checks if email is in all_emails list and adds it if it isn't
		"""

		email = email.strip()
		if email  not in self.all_emails:
			self.debug_print("Adding found email: " + email)
			self.all_emails.append(email)

	def print_emails(self):
		""" Prints all found emails
		"""
		if self.all_emails:
			print "Found these email addresses:"
			for email in self.all_emails:
				print email
		else:
			print "No Emails Found"
	def debug_print(self, text):
		""" Prints debugging code if self.debug is True
		"""

		if self.debug:
			print text



if __name__ == '__main__':
	domain = sys.argv[1]
	email_finder = Email_Finder(False)
	email_finder.process_domain(domain)
	