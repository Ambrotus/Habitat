import os
import sys
import re
import json
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests

# #imports

# testing urls
# url = 'https://rentals.ca/etobicoke/92-james-st';
# url = 'https://rentals.ca/north-york/9-kingsbridge-court'
url = 'https://rentals.ca/toronto/368-eglinton-avenue-east'

# header to have our client be read as a browser and pretend to be a real person
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}

# create an HTML Session object
# session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'"])
session = HTMLSession(browser_args=[
    "--user-Agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'",
    "--accept= 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'",
    "--accept-Language= 'en-US,en;q=0.5'",
    "--referer = 'https://www.google.com/'",
    "--DNT= '1'",
    "--connection = 'keep-alive'",
    "--upgrade-Insecure-Requests = '1'"
])
# Use the object above to connect to needed webpage
resp = session.get(url)

# print resp should return <Response [200]>
print(resp)
# testing response from website
test1 = resp.status_code == 200
if test1 == True:
    print("Test 1 passed, Response 200 received")
    print("Connection Achieved")
else:
    print("Test 1 failed, Response 200 not received")
    print("Connection failed")


# Run JavaScript code on webpage
resp.html.render()
# grab the page into an object we can search
soup = BeautifulSoup(resp.html.html, "lxml")

# Get page info
floorPlans = soup.find_all(class_="menu-panel-slider listing-floor-plans")
aboutListing = soup.find_all(class_="listing-highlighted-info")
listingText = soup.find_all(class_="truncated-content text-lines")
listingSummary = soup.find_all(class_="listing-summary")
# for finding address
# <h1 class="listing-card-bar__address">
#       $500 MOVE-IN BONUS! 368 Eglinton Avenue East - Toronto, ON
#     # </h1>
# finds property type and age of posting
listingInfo = soup.find_all(class_="listing-card-bar__descriptor")
# for finding about pet friendly
petInfo = soup.find_all(class_="listing-card-bar__features")
addressInfo = soup.find(class_="listing-card-bar__address")

# listingUrl.get('href')
soup.find_all(class_="menu-panel-slider__panel")
floorPlanList = []
for i in range(len(floorPlans[0].contents[0])):
    floorPlanList.append({
        "Type":         floorPlans[0].contents[0].contents[i].contents[0].contents[2].next,
        "Price":        floorPlans[0].contents[0].contents[i].contents[0].contents[0].next,
        #  subMenu    floorplan
        "Bedrooms":     floorPlans[0].contents[2].contents[i].contents[2].contents[0].contents[2].next,
        "Bathrooms":    floorPlans[0].contents[2].contents[i].contents[2].contents[2].contents[2].next,
        "Size":         re.sub("^[ \s]+|[ \s]+$", "", floorPlans[0].contents[2].contents[i].contents[2].contents[4].contents[2].next),
        "Availability": floorPlans[0].contents[2].contents[i].contents[2].contents[6].contents[2].next
    })

# featuresAndAmenities = soup.find_all(class_="listing-features-and-amenities__content")
# listing-features-and-amenities__content
# buildingFeaturesList = []
# for item in featuresAndAmenities[0].contents:
#   buildingFeaturesList.append(item.text)
# unitFeaturesList = []
# for item in featuresAndAmenities[1].contents:
#   unitFeaturesList.append(item.text)
# nearbyFeaturesList = []
# for item in featuresAndAmenities[2].contents:
#   nearbyFeaturesList.append(item.text)
# otherFeaturesList = [] #https://rentals.ca/etobicoke/92-james-st
# for item in featuresAndAmenities[3].contents:
#   otherFeaturesList.append(item.text)
# utilitiesList = []

petFriendlyStatus = "No"
for i in range(len(petInfo[0].contents)):
    if petInfo[0].contents[i] != ' ':
        petInfoText = re.sub("[^A-Za-z]", "", petInfo[0].contents[i].text)
        if petInfoText == "Pets":
            petFriendlyStatus = "Yes"
    #numberOfListings = int(re.sub("\S","",numberOfListings[0].text))
# petFriendlyStatus =petInfo[0].contents[4].text, # " pets" might not work all the time maybe use a for loop to find the word pets otherwise leave empty

# include posting date thats on the page also some pages have features and amenities/ building features and utilities included that should be
# added https://rentals.ca/etobicoke/45-morgan-avenue-1 and https://rentals.ca/toronto/368-eglinton-avenue-east as they have differing data will need catches probs
listingJson = {
    "Url":                url,

    # address
    # should work every time
    "Address":            re.sub("^[ \s]+|[ \s]+$", "", addressInfo.text),
    # property type
    # should work every time
    "Property Type":      listingInfo[0].contents[2].text,
    # age of posting
    # should work every time
    "Age of Posting":     re.sub("^[ \s]+|[ \s]+$", "", listingInfo[0].contents[4].text),
    # pet friendly
    "Pet Friendly":       petFriendlyStatus,

    # floorPlanArray
    "Floor Plans":       floorPlanList,  # should work every time

    # features & amenities *******todo  might not work every time
    "Building Features":  "Visit url for more info",  # buildingFeaturesList,
    "Unit Features":      "Visit url for more info",  # unitFeaturesList,
    "Nearby Features":    "Visit url for more info",  # nearbyFeaturesList,
    "Other Features":     "Visit url for more info",  # otherFeaturesList,
    # utilities
    "Utilities Included": "Visit url for more info",  # utilitiesList,

    # aboutListing
    # should work every time
    "Property Type":      aboutListing[0].contents[0].contents[2].next,
    # should work every time
    "Property Sub-type":  aboutListing[0].contents[2].contents[2].next,
    # should work every time
    "Parking Type":       aboutListing[0].contents[4].contents[2].next,
    # should work every time
    "Parking Spots":      aboutListing[0].contents[6].contents[2].next,
    # should work every time
    "Lease Term":         aboutListing[0].contents[8].contents[2].next,
    # should work every time
    "Short-term":         aboutListing[0].contents[10].contents[2].next,
    # should work every time
    "Furnished":          aboutListing[0].contents[12].contents[2].next,
    # should work every time
    "Year Built":         aboutListing[0].contents[14].contents[2].next,
    # should work every time
    "Summary":            re.sub("^[ \s]+|[ \s]+$", "", listingSummary[0].text)
}

# f = open('jsontest.json',)
# testData = json.load(f)

# test2 = listingJson == testData
# if test2 == True:
#     print("Test 2 passed, Test Data is the same as the data received from the website")
# else:
#     print("Test 2 failed, Test Data differs from the data received from the website")
#     print("Try new header or vpn")


# create test file and single json file for the listing
print()
print("----------")
print(json.dumps(listingJson))
f = open("jsontest.json", "w")
f.write(json.dumps(listingJson))
f.close()
