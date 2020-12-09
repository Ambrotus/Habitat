# imports
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import prettify
import json
import re
import sys
import getopt
from random import randint
from time import sleep
import time

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm

# returns an array/list of urls
def getUrlsForCity(argv):
    # https://rentals.ca/toronto?sort=updated&p=1
    # this will get the most recent in order of date
    city =""
    urls = []

    try:
        city = argv[1]
    except:
        print("Proper usage: \nrentalsCrawlerAndScraper.py -getUrlsForCity city")

    url = 'https://rentals.ca/%s?p=1' % city

    # create an HTML Session object
    session = HTMLSession(browser_args=[
        "--user-Agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'",
        "--accept= 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'",
        "--accept-Language= 'en-US,en;q=0.5'",
        "--referer = 'https://www.google.com/'",
        "--DNT= '1'",
        "--connection = 'keep-alive'",
        "--upgrade-Insecure-Requests = '1'",
    ])

    # Use the object above to connect to needed webpage
    resp = session.get(url)
    # resp = request(session=session, method='POST', data=data, allow_redirects=True,)
    # session.close()
    # Run JavaScript code on webpage
    resp.html.render()  # need to catch exception here!!!!!!!!!!!!!
    # grab the page into an object we can search
    soup = BeautifulSoup(resp.html.html, "lxml")
    # Get page urls
    anchoredUrls = soup.find_all(class_="listing-card__details-link")

    urls = []
    for url in anchoredUrls:
        urls.append(url.get('href'))

    # 9210
    numberOfListings = soup.find_all(class_="page-title__bottom-line")
    numberOfListings = int(re.sub("\D", "", numberOfListings[0].text))
    numberOfPages = int(numberOfListings / 10)
    if ((numberOfListings % 10) > 0):
        numberOfPages += 1

    if numberOfPages > 1:
        for i in range(numberOfPages):
            url = 'https://rentals.ca/%s?p=%d' % (city, i+2)
            # Use the object above to connect to needed webpage
            session = HTMLSession(browser_args=[
                "--user-Agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'",
                "--accept= 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'",
                "--accept-Language= 'en-US,en;q=0.5'",
                "--referer = 'https://www.google.com/'",
                "--DNT= '1'",
                "--connection = 'keep-alive'",
                "--upgrade-Insecure-Requests = '1'"
            ])
            resp = session.get(url)
            # Run JavaScript code on webpage
            resp.html.render()
            # grab the page into an object we can search
            soup = BeautifulSoup(resp.html.html, "lxml")
            # Get page urls
            anchoredUrls = soup.find_all(class_="listing-card__details-link")

            for listingUrl in anchoredUrls:
                urls.append(listingUrl.get('href'))
            resp.close
            session.close
            time.sleep(1) #10 seconds
            if i == 0:
                break
    print(urls)
    resp.close
    session.close

    empty = ""
    postings = []
    for url in urls:
        listing = {
            "Url":               url,
            # address
            "Address":           empty,
            # age of posting
            "AgeOfPosting":      empty,
            # pet friendly
            "PetFriendly":       empty,
            # floorPlanArray
            "FloorPlans":        empty,  # should work every time
            # features & amenities *******todo  might not work every time so i removed it
            "BuildingFeatures":  empty,  # buildingFeaturesList,
            "UnitFeatures":      empty,  # unitFeaturesList,
            "NearbyFeatures":    empty,  # nearbyFeaturesList,
            "OtherFeatures":     empty,  # otherFeaturesList,
            # utilities
            "UtilitiesIncluded": empty,  # utilitiesList,
            # aboutListing
            "PropertyType":      empty,
            "PropertySubType":  empty,
            "ParkingType":       empty,
            "ParkingSpots":      empty,
            "LeaseTerm":         empty,
            "ShortTerm":        empty,
            "Furnished":         empty,
            "YearBuilt":         empty,
            "Summary":           empty
        }
        postings.append(listing)
    f = open("%sListings.json" % city, "w")
    fileToWrite = postings
    f.write(json.dumps(fileToWrite))
    f.close()


    return urls
#  end of geturls()--------------------------------

# argv[1], argv[2],argv[3],argv[4]
# urlToScrape, test1, test2, createTestData
def testScrapeUrl(argv):
    # testing urls
    # url = 'https://rentals.ca/etobicoke/92-james-st';
    # url = 'https://rentals.ca/north-york/9-kingsbridge-court'
    # url = 'https://rentals.ca/toronto/368-eglinton-avenue-east'
    url = argv[1]

    # create an HTML Session object with header to have our client be read as a browser and pretend to be a real browser
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

    # Run JavaScript code on webpage
    resp.html.render()

    # test1 for testing response from website
    if argv[2] == "True":
        # print(resp) resp should return <Response [200]> if the connection was established
        test1 = resp.status_code == 200
        if test1 == True:
            print("Test 1 passed, Response 200 received")
            print("Connection Achieved")
        else:
            print("Test 1 failed, Response 200 not received")
            print("Connection failed")

    # grab the page into an object we can search
    soup = BeautifulSoup(resp.html.html, "lxml")

    # Get rental info
    floorPlans = soup.find_all(class_="menu-panel-slider listing-floor-plans")
    aboutListing = soup.find_all(class_="listing-highlighted-info")
    listingText = soup.find_all(class_="truncated-content text-lines")
    listingSummary = soup.find_all(class_="listing-summary")
    # finds property type and age of posting
    listingInfo = soup.find_all(class_="listing-card-bar__descriptor")
    petInfo = soup.find_all(class_="listing-card-bar__features")
    addressInfo = soup.find(class_="listing-card-bar__address")

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

    petFriendlyStatus = "No"
    for i in range(len(petInfo[0].contents)):
        if petInfo[0].contents[i] != ' ':
            petInfoText = re.sub("[^A-Za-z]", "", petInfo[0].contents[i].text)
            if petInfoText == "Pets":
                petFriendlyStatus = "Yes"

    listingJson = {
        "Url":                url,
        # address
        "Address":            re.sub("^[ \s]+|[ \s]+$", "", addressInfo.text),
        # property type
        # age of posting
        "AgeOfPosting":     "skip this for testing",
        # pet friendly
        "PetFriendly":       petFriendlyStatus,
        # floorPlanArray
        "FloorPlans":       floorPlanList,
        # features & amenities
        "BuildingFeatures":  "Visit url for more info",  # buildingFeaturesList,
        "UnitFeatures":      "Visit url for more info",  # unitFeaturesList,
        "NearbyFeatures":    "Visit url for more info",  # nearbyFeaturesList,
        "OtherFeatures":     "Visit url for more info",  # otherFeaturesList,
        # utilities
        "UtilitiesIncluded": "Visit url for more info",  # utilitiesList,
        # aboutListing
        "PropertyType":      aboutListing[0].contents[0].contents[2].next,
        "PropertySubType":  aboutListing[0].contents[2].contents[2].next,
        "ParkingType":       aboutListing[0].contents[4].contents[2].next,
        "ParkingSpots":      aboutListing[0].contents[6].contents[2].next,
        "LeaseTerm":         aboutListing[0].contents[8].contents[2].next,
        "ShortTerm":         aboutListing[0].contents[10].contents[2].next,
        "Furnished":          aboutListing[0].contents[12].contents[2].next,
        "YearBuilt":         aboutListing[0].contents[14].contents[2].next,
        "Summary":            re.sub("^[ \s]+|[ \s]+$", "", listingSummary[0].text)
    }

    # test2 for comparing page data from website against local data
    if argv[3] == "True":
        f = open('jsontest.json',)
        testData = json.load(f)

        test2 = listingJson == testData
        if test2 == True:
            print(
                "Test 2 passed, Test Data is the same as the data received from the website")
        else:
            print(
                "Test 2 failed, Test Data differs from the data received from the website")
            print("Try new header or vpn")

    # create single test json file for the listing
    if argv[4] == "createTestData":
        print()
        print("----------")
        print(json.dumps(listingJson))
        f = open("jsontest.json", "w")
        f.write(json.dumps(listingJson))
        f.close()
# end of ScrapeUrl() ------------------

def fillCityListings(argv):
    try:
        cityFileName = argv[1]
    except:
        print("Proper usage: \nrentalsCrawlerAndScraper.py -fillCityListings city")

    jsonFile = open('%sListings.json' % cityFileName,)
    cityData = json.load(jsonFile)
    postings = []
    for listing in cityData:
        url = listing.get("Url")
        loadAttempt = 0
        loadSucceeded = False
        if loadSucceeded == False:
            try:
                # Use the object above to connect to needed webpage
                session = HTMLSession(browser_args=[
                    "--user-Agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'",
                    "--accept= 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'",
                    "--accept-Language= 'en-US,en;q=0.5'",
                    "--referer = 'https://www.google.com/'",
                    "--DNT= '1'",
                    "--connection = 'keep-alive'",
                    "--upgrade-Insecure-Requests = '1'"
                ])
                resp = session.get(url)
                # Run JavaScript code on webpage
                resp.html.render()
                # META NAME="robots"
                # Use the find method in Python 2.7 or Python 3.6
                if resp.text.find('<META NAME="ROBOTS"') != -1:
                    print("The scrape was blocked!")
                else:
                    print("The scrape succeeded, proceeding to add data!")
                    loadSucceeded = True

            except :
                print("%s failed, trying again" % url)
                loadAttempt +=1
                if loadAttempt == 3:
                    empty = ""
                    listing = {
                        "Url":               url,
                        # address
                        "Address":           empty,
                        # age of posting
                        "AgeOfPosting":      empty,
                        # pet friendly
                        "PetFriendly":       empty,
                        # floorPlanArray
                        "FloorPlans":        empty,  # should work every time
                        # features & amenities
                        "BuildingFeatures":  empty,  # buildingFeaturesList,
                        "UnitFeatures":      empty,  # unitFeaturesList,
                        "NearbyFeatures":    empty,  # nearbyFeaturesList,
                        "OtherFeatures":     empty,  # otherFeaturesList,
                        # utilities
                        "UtilitiesIncluded": empty,  # utilitiesList,
                        # aboutListing
                        "PropertyType":      empty,
                        "PropertySubType":  empty,
                        "ParkingType":       empty,
                        "ParkingSpots":      empty,
                        "LeaseTerm":         empty,
                        "ShortTerm":        empty,
                        "Furnished":         empty,
                        "YearBuilt":         empty,
                        "Summary":           empty
                    }
                    postings.append(listingJson)
                    break

        if loadSucceeded:
            # grab the page into an object we can search
            soup = BeautifulSoup(resp.html.html, "lxml")
            try:
                # Get rental info
                floorPlans = soup.find_all(class_="menu-panel-slider listing-floor-plans")
                aboutListing = soup.find_all(class_="listing-highlighted-info")
                listingText = soup.find_all(class_="truncated-content text-lines")
                listingSummary = soup.find_all(class_="listing-summary")
                # finds property type and age of posting
                listingInfo = soup.find_all(class_="listing-card-bar__descriptor")
                petInfo = soup.find_all(class_="listing-card-bar__features")
                addressInfo = soup.find(class_="listing-card-bar__address")

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

                petFriendlyStatus = "No"
                for i in range(len(petInfo[0].contents)):
                    if petInfo[0].contents[i] != ' ':
                        petInfoText = re.sub("[^A-Za-z]", "", petInfo[0].contents[i].text)
                        if petInfoText == "Pets":
                            petFriendlyStatus = "Yes"

                listingJson = {
                    "Url":              url,
                    # address
                    "Address":          re.sub("^[ \s]+|[ \s]+$", "", addressInfo.text),
                    # age of posting
                    "AgeOfPosting":     re.sub("^[ \s]+|[ \s]+$", "", listingInfo[0].contents[4].text),
                    # pet friendly
                    "PetFriendly":      petFriendlyStatus,
                    # floorPlanArray
                    "FloorPlans":       floorPlanList,
                    # features & amenities
                    "BuildingFeatures":  "Visit url for more info",  # buildingFeaturesList,
                    "UnitFeatures":      "Visit url for more info",  # unitFeaturesList,
                    "NearbyFeatures":    "Visit url for more info",  # nearbyFeaturesList,
                    "OtherFeatures":     "Visit url for more info",  # otherFeaturesList,
                    # utilities
                    "UtilitiesIncluded": "Visit url for more info",  # utilitiesList,
                    # aboutListing
                    "PropertyType":      aboutListing[0].contents[0].contents[2].next,
                    "PropertySubType":  aboutListing[0].contents[2].contents[2].next,
                    "ParkingType":       aboutListing[0].contents[4].contents[2].next,
                    "ParkingSpots":      aboutListing[0].contents[6].contents[2].next,
                    "LeaseTerm":         aboutListing[0].contents[8].contents[2].next,
                    "ShortTerm":        aboutListing[0].contents[10].contents[2].next,
                    "Furnished":         aboutListing[0].contents[12].contents[2].next,
                    "YearBuilt":         aboutListing[0].contents[14].contents[2].next,
                    "Summary":           re.sub("^[ \s]+|[ \s]+$", "", listingSummary[0].text)
                }
            except:
                print("exception parsing info at %s " % url)

        session.close
        resp.close
        postings.append(listingJson)
        sleep(randint(5,60))
    jsonFile.close()
    print(json.dumps(postings))
    f = open('%sListings.json' % cityFileName,"w")
    f.write(json.dumps(postings))
    f.close()

def main(argv):
    default = print
    # https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python  5th one down
    choices = {
        "-testScrapeUrl" : testScrapeUrl,
        "-getUrlsForCity" : getUrlsForCity,
        "-fillCityListings" : fillCityListings
    }
    result = choices.get(argv[0],default)
    try:
        result(argv)
    except :
        print('USAGE \nrentalsCrawlerAndScraper.py -functionName bool bool createTestData \nor \nrentalsCrawlerAndScraper.py -getUrlsForCity city \nor \nrentalsCrawlerAndScraper.py -testScrapeUrl url test1bool test2bool createTestDataBool')

if __name__ == "__main__":
   main(sys.argv[1:])
# main()