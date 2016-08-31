# challenge_Sept_2016
This code finds all the email addresses on a given domain

# Setup
To install the required libraries, run `pip install -r requirements.txt`

# Running the Code

To run the code, run `python find_email_addresses.py jana.com` 

This will run the code, but only searching internal links found from the homepage. To search all internal links throughout the site, run `python find_email_addresses.py jana.com -f`
web.mit.edu has been internal links, for example. Searching through all of them is time-consuming and does not appear to be what your sample data is looking for. jana.com has fewer internal links so it can be run either way. At this point, running this code with -f on web.mit.edu will take a very long time and eventually fail because a link redirects too many times. 

To run the code in debug mode and get some basic debugging notes on what is going on, run `python find_email_addresses.py jana.com -d`

To use both of the flags, run `python find_email_addresses.py jana.com -df`

# Notes

The challenge said not to crawl subdomains, yet I wasn't sure how to handle mit.edu with web.mit.edu. In the end, I don't check any subdomains, which includes web.mit.edu if mit.edu is the domain passed in. When web.mit.edu, the whole domain is parsed. It would not be a major change to handle redirects on the domain only, but I have not done that. Let me know if I should. 

Of note, this is my first time really using regular expressions. I did choose to use them so it's not an excuse for any mistakes, but if you see something that I overcomplicated or should have done differently, this would be the reason. 

I assumed using online resources was acceptable. There were multiple stackoverflow answers that were especially helpful, especially in using regex to find email addresses. Having never used regex, I probably wouldn't have been able to complete the challenge as effectively without the following pages:
 http://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
 http://stackoverflow.com/questions/13482777/when-i-use-python-requests-to-check-a-site-if-the-site-redirects-me-to-another
 I am not sure if this is an issue, but I felt like not disclosing them would be considered cheating. 