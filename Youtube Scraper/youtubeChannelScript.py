# Nooras Fatima 
# https://github.com/nooras

#Importing all libraries
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs4
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import pandas as pd
import re
import requests
import urllib.parse
from time import sleep
import csv
import pymongo
from bson.objectid import ObjectId
import sys

#Use Incognito mode when scraping
chrome_options = Options()
chrome_options.add_argument(" — incognito")
browser = webdriver.Chrome(options=chrome_options)

#Search and getting the page data
# SearchWord = "cancer"
SearchWord = sys.argv[1] 
url = "https://www.youtube.com/results?search_query=" + SearchWord
browser.get(url)

x = browser
x.page_source
aTag = x.find_elements_by_xpath('//*[@id="video-title"]') #Finding div of video-title 

#Saving all videoName And VideoHref in aAttribute dict
aAttribute = {}
for a in aTag:
    videoTitle = a.get_attribute("title")
    videoHref = a.get_attribute("href")
    aAttribute[videoTitle] = videoHref

#Function for getting channel Name and Channel href
def browseChannelUrl(urlBrowse):
    browser.get(urlBrowse)
    browser.page_source
    channel = browser.find_element_by_xpath('//*[@id="text"]/a')
    channelName = channel.text
    channelHref = channel.get_attribute('href')
    #print(channelName, channelHref)
    return channelName, channelHref

# a, b = browseChannelUrl('https://www.youtube.com/watch?v=SGaQ0WwZ_0I')
# print(a,b)

#Function for Retrieving all link from about page
def aboutRetrieveUrl(urlChannel):
    #link = {}
    browser.get(urlChannel)
    browser.page_source
    text_list = browser.find_elements_by_xpath("//div[@class='tab-content style-scope paper-tab']")  
    btn = text_list[-1]    # Fetching the text of last element
    btn.click()
    browser.page_source
    data = browser.find_element_by_xpath('//*[@id="links-container"]') 
    aTags = data.find_elements_by_tag_name('a')
    l = [{"Link_Name":a.text, "Link":a.get_attribute('href')} for a in aTags]
    # for a in aTags:
    #     #print(a.text, a.get_attribute('href'))
    #     link[a.text] = a.get_attribute('href')
    return l
    
#aboutRetrieveUrl('https://www.youtube.com/channel/UCkNrj1l4JLvLX7M42fJoLGw')

#Mongodb Connection
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz #db
YTData = db.youtubeScriptData #collection

#Going thourgh all dict aAttribuue dict for retrieving all necessary data and saving it in CSV file and into the db
with open('YTScriptData.csv', mode='w') as csv_file:
    fieldnames = ['VideoTitle', 'VideoHref', 'ChannelName', 'ChannelHref', 'Links']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for key, value in aAttribute.items(): #dict
        videoTitle = key
        videoHref = value
        sleep(1)
        chanelName, channelHref = browseChannelUrl(videoHref)
        sleep(1)
        aboutLinks = aboutRetrieveUrl(channelHref)
        sleep(1)
        #print(videoTitle, videoHref)
        #print(chanelName, channelHref)
        #print(aboutLinks)
        writer.writerow({'VideoTitle': videoTitle, 'VideoHref': videoHref, 'ChannelName': chanelName, 'ChannelHref':channelHref, 'Links':aboutLinks}) #inserting in csv file
        YTData.insert({'VideoTitle': videoTitle, 'VideoHref': videoHref, 'ChannelName': chanelName, 'ChannelHref':channelHref, 'Links':aboutLinks}, check_keys=False) #Inserting in db
        print("-----One Document Inserted.------")
