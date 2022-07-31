
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape():


    scraped_data = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(1)
    # driver = webdriver.Chrome("/Users/alexanderpowers/Downloads/chromedriver")
    # driver.get(url)
    # html = driver.page_source
    html = browser.html
    soup = bs(html, 'html.parser')

    titles = soup.find_all('div', class_="content_title")
    paragraphs = soup.find_all('div', class_="article_teaser_body")
    news_title = titles[0].text
    news_p = paragraphs[0].text
    scraped_data["news_title"]=news_title
    scraped_data["news_p"]=news_p

    browser.quit()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('img',class_="headerimage fade-in")
    featured_image_url = image.get('src')
    featured_image_url = f"https://spaceimages-mars.com/{featured_image_url}"
    scraped_data["featured_image_url"]=featured_image_url

    browser.quit()

    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    table = tables[0]
    table_html_string = table.to_html(header=True)
    scraped_data["table_html_string"]=table_html_string

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    pages = ["cerberus.html","schiaparelli.html","syrtis.html","valles.html"]
    url = 'https://marshemispheres.com/'

    hemisphere_image_urls = []

    for page in pages:

        browser.visit(url + page)
        html = browser.html
        soup = bs(html, 'html.parser')

        image = soup.find('img', class_='thumb')
        image_url = image.get('src')
        image_url = f"https://marshemispheres.com/{image_url}"

        title = soup.find('h2', class_='title').text
        hemisphere_image_dict = {"title":title,"img_url":image_url}
        hemisphere_image_urls.append(hemisphere_image_dict)

    scraped_data["hemisphere_image_urls"]=hemisphere_image_urls
    browser.quit()
    return scraped_data

scrape()