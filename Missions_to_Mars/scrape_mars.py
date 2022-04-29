#!/usr/bin/env python
# coding: utf-8

# # MISSION TO MARS 

# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # # NASA Mars News 

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    # find the first news title
    news_title = soup.find("div", class_="content_title").text
    # find the paragraph associated with the first title
    news_p = soup.find("div", class_="article_teaser_body").text

    # # JPL Mars Space Images - Featured Image

    # URL of page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    relative_image_path = soup.find_all('a')[2]["href"]
    featured_image_url = url + relative_image_path

    # # Mars Facts

    import pandas as pd

    # URL of page to be scraped
    url = 'https://galaxyfacts-mars.com/'

    # Read the tables 
    tables = pd.read_html(url)

    # Select the first table
    df=tables[0]

    # Rename the columns 
    df.columns = ["Info", "Mars", "Earth"]

    #Drop the index
    df = df.iloc[1:]

    #convert to html table
    html_table = df.to_html()

    # Use Pandas to convert the data to a HTML table string 
    df.to_html('table.html')

    # # Mars Hemispheres

    # URL of page to be scraped
    url = "https://marshemispheres.com/"
    browser.visit(url)    
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Find all image titles 
    title_list = []
    titles = soup.find_all("h3")
    print(titles)

    # Loop through the image titles and append them to the list 
    for title in titles:
        title_list.append(title.text)

        print(title.text)


    # Print only first 4 titles
    title_list = title_list[0:4]

    image_list = []

    for title in title_list:
        url = "https://marshemispheres.com/"
        browser.visit(url)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(browser.html, 'html.parser')
        image_url = soup.find_all("li")[0].a["href"]
        dict1 = {"title":title, "image_url": image_url}
        image_list.append(dict1)
        
    # Store Data in a dictionary
    mars_data = {"news_title": news_title,
        "News_paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Facts": html_table,
        "Hemispheres": image_list
         }

    return mars_data

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape())

