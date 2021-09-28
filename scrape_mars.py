# Import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # visit site and scrape
    site_url = "https://mars.nasa.gov/news/"
    browser.visit(site_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #Scrape the Mars News Site and collect the latest News Title and Paragraph Text. 
    #Assign the text to variables that you can reference later.

    article = soup.find("div", class_="list_text")
    summary = article.find("div", class_="article_teaser_body").text
    title = article.find("div", class_="content_title").text
    date = article.find("div", class_="list_date").text

    # Add the news date, title and summary to the dictionary
    mars_data["date"] = date
    mars_data["title"] = title
    mars_data["summary"] = summary

    # Visit the url for the Featured Space Image site
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    # Assign the url string to a variable called featured_image_url
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find("img", class_="headerimage fade-in")["src"]
    img_url = "https://spaceimages-mars.com/"+image
    featured_image_url = img_url

    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    df = pd.read_html("https://galaxyfacts-mars.com/")[1]
    df.columns= ["Description", "Mars"]
    df.set_index("Description", inplace=True)
    mars_facts = df.to_html()

    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = mars_facts

    # Visit the astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    astro_url = "https://marshemispheres.com/"
    browser.visit(astro_url)

    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
    #Use a Python dictionary to store the data using the keys img_url and title.


    hemisphere_image_urls = []

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://marshemispheres.com/'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = hemisphere_image_urls
    # Return the dictionary
    return mars_data
