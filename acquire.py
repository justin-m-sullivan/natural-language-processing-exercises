import pandas as pd
import re
import requests
import bs4

urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/', 'https://codeup.com/data-science-myths/', 
        'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/', 'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
        'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

def get_blog_articles(urls):
    '''
    This function takes in a list of URLS of codeup's blogs and 
    returns a list of dictionaries with each dictionary containing the title
    and content of each blog from the urls
    '''
    output = {}
    
    for url in urls:
        headers = {'User-Agent': 'Codeup Data Science'}
        response = requests.get(url, headers=headers)
        html = response.text
        soup = bs4.BeautifulSoup(html)
        
        blog_container = soup.select('.jupiterx-post')
        blog = blog_container[0]
        
        blog_dict = {"title": blog.find('h1').text,
        "content": blog.select('.jupiterx-post-content')[0].text}
        
        output.append(blog_dict)
        
    return  output


def get_article(article, category):
    # Attribute selector
    title = article.select("[itemprop='headline']")[0].text
    
    # article body
    content = article.select("[itemprop='articleBody']")[0].text
    
    output = {}
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    return output


def get_articles(category):
    """
    This function takes in a category as a string. Category must be an available category in inshorts
    Returns a list of dictionaries where each dictionary represents a single inshort article
    """
    base = "https://inshorts.com/en/read/"
    
    # We concatenate our base_url with the category
    url = base + category
    
    # Set the headers to show as Netscape Navigator on Windows 98, b/c I feel like creating an anomaly in the logs
    headers = {"User-Agent": "Codeup-data-science"}

    # Get the http response object from the server
    response = get(url, headers=headers)

    # Make soup out of the raw html
    soup = BeautifulSoup(response.text)
    
    # Ignore everything, focusing only on the news cards
    articles = soup.select(".news-card")
    
    output = []
    
    # Iterate through every article tag/soup 
    for article in articles:
        
        # Returns a dictionary of the article's title, body, and category
        article_data = get_article(article, category) 
        
        # Append the dictionary to the list
        output.append(article_data)
    
    # Return the list of dictionaries
    return output


def get_all_news_articles(categories):
    """
    Takes in a list of categories where the category is part of the URL pattern on inshorts
    Returns a dataframe of every article from every category listed
    Each row in the dataframe is a single article
    """
    all_inshorts = []

    for category in categories:
        all_category_articles = get_articles(category)
        all_inshorts = all_inshorts + all_category_articles

    df = pd.DataFrame(all_inshorts)
    return df
