# webscraper.py
# ** under development. This is just test code**

# #imports
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import prettify


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
    #'User-Agent': 'Mozilla/5.0'}
#http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
# create an HTML Session object
url = 'https://rentals.ca/etobicoke/92-james-st';
# url = "https://4rent.ca/Toronto-High-Rise-Apartment-77-Gerrard-West-4R3668/#21"

session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'"])

# Use the object above to connect to needed webpage
# resp = session.get("https://finance.yahoo.com/quote/NFLX/options?p=NFLX")
resp = session.get(url)

# Run JavaScript code on webpage
resp.html.render()
soup = BeautifulSoup(resp.html.html, "lxml")
# https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
# https://www.kite.com/python/examples/4419/beautifulsoup-find-an-element-by-its-id
option_tags = soup.find_all(class_="page-listing-details__container-bottom")

dates = [tag.text for tag in option_tags]

# javascript:__doPostBack('Listing1$ctlLBTViewAll','')
print(dates)
# print(soup.prettify())

#


# print("Hello world")

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
    #'User-Agent': 'Mozilla/5.0'}
# headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

# headers ={
#   "headers": {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Dnt": "1",
#     "Host": "httpbin.org",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
#     "X-Amzn-Trace-Id": "Root=1-5f879504-1604740202bfcee437d589f3"
#   }
# }
#"origin": "66.115.189.227",
#"url": "http://httpbin.org/get"

# url = "https://4rent.ca/Toronto-High-Rise-Apartment-77-Gerrard-West-4R3668/#21"

# r = requests.get(url, headers=headers)
# print(r.text)

# soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.prettify())
