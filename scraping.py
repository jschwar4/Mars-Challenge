#!/usr/bin/env python
# coding: utf-8

# In[15]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import lxml


# In[18]:


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(browser),
      "last_modified": dt.datetime.now()
    }
       # Stop webdriver and return data
    browser.quit()
    return data


# In[12]:


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html,'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div',class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


# In[13]:


def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    #select the second button to get thte full size image page
    full_image_elem = browser.find_by_tag('button')[1]
    #click on the image element
    full_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #pull the image from the webpage
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


# In[16]:


def mars_facts(browser):
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html()


# In[ ]:


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

# 1. Use browser to visit the URL 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
def image_urls(browser):
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html_soup = soup(html, 'html.parser')
    image_pages = html_soup.find_all('a', class_="itemLink product-item")
    
    for page in image_pages:
        hemisphere = {}
        url = 'https://marshemispheres.com/'
        page_url = url+page.get('href')
        browser.visit(page_url)
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')
        try:
            hemisphere_image = hemisphere_soup.find('li')
            hemisphere_title = hemisphere_soup.find('h2').get_text(strip=True)
        except AttributeError:
            print("exception")
        hemisphere[hemisphere_title] = hemisphere_image
        hemisphere_image_urls.append(hemisphere)
image_urls(browser)

# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()