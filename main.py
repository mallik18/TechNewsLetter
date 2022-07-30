import requests
import xmltodict
from bs4 import BeautifulSoup
from collections import namedtuple
from urllib.request import urlopen
import pprint


Article = namedtuple("Article", "title link")

# Engineering articles
NETFLIX_ENGINEERING = "https://netflixtechblog.com"
UBER_ENGINEERING = "https://eng.uber.com"
YELP_ENGINEERING = "https://engineeringblog.yelp.com/"
META_ENGINEERING = "https://engineering.fb.com/feed/"
DATABRICKS = "https://databricks.com/blog/category/engineering"
AMAZON_DATABASES = "https://aws.amazon.com/blogs/database/"


def get_netflix_articles():
    articles = []
    page = requests.get(NETFLIX_ENGINEERING)
    soup = BeautifulSoup(page.content, "html.parser")
    articles_container = soup.find_all("div", class_=
                         "u-marginBottom40 js-collectionStream")[0]

    articles_sections = list(articles_container.find_all("div",
                        class_="streamItem streamItem--section js-streamItem"))

    for section in articles_sections:
        articles.extend(Article(title=element.find_all("div")[0].text,
                        link=element["href"]) for element in
                        section.find_all("a")
                        if element.has_attr("data-post-id"))

    return articles[:3]


def get_uber_articles():
    page = requests.get(UBER_ENGINEERING, headers=
                        {'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(page.content, "html.parser")

    article_links = soup.find_all("a", {"rel": "bookmark"})
    articles = [Article(title=article.text, link=article["href"])
                        for article in article_links]

    return articles[:3]


def get_yelp_articles():
    articles = []
    page = requests.get(YELP_ENGINEERING, headers=
                        {'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(page.content, "html.parser")
    all_posts = soup.find_all("div", class_="posts")[0].find_all("article")
    for article in all_posts:
        article_link = article.find_all("a")[0]["href"]
        articles.append(
            Article(
                link=f"{YELP_ENGINEERING}/{article_link}",
                title=article.find_all("a")[0].text
            )
        )
    return articles[:5]


def get_meta_articles():
    articles = []
    file = urlopen(META_ENGINEERING)
    data = file.read()
    file.close()

    data = xmltodict.parse(data)["rss"]["channel"]
    for key, value in data.items():
        if key == "item":
            site_data = value
            articles.extend(Article(title=item["title"], link=item["link"])
                                    for item in site_data)

    return articles[:5]


def get_databricks_articles():
    articles = []
    page = requests.get(DATABRICKS, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, "html.parser")
    all_posts = soup.find_all("div", class_="blog-content")[0].find_all("h2",
                               class_="blog-post--header--title")
    for post in all_posts:
        a_tag = post.find_all("a")[0]
        articles.append(
            Article(
                title=a_tag.text,
                link=a_tag["href"]
            )
        )
    return articles[:5]


def get_amazon_databases_articles():
    articles = []
    page = requests.get(AMAZON_DATABASES, headers=
                        {'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(page.content, "html.parser")
    all_posts = soup.find_all("article", class_="blog-post")
    for post in all_posts:
        a_tag = post.find_all("h2", class_=
                              "blog-post-title")[0].find_all("a")[0]
        articles.append(
            Article(
                title=a_tag.text,
                link=a_tag["href"]
            )
        )
    return articles

def tech_news():
    print("Starting to scrape..")
    uber_articles = get_uber_articles()
    netflix_articles = get_netflix_articles()
    yelp_articles = get_yelp_articles()
    meta_articles = get_meta_articles()
    databricks_articles = get_databricks_articles()
    aws_db_articles = get_amazon_databases_articles()

    software_engineering_articles = uber_articles + \
        netflix_articles + yelp_articles + meta_articles\
        + databricks_articles + aws_db_articles

    print(f"Scraped {len(software_engineering_articles)} \
            software engineering articles.")

    print("Sending Email")

    email_body = "Here are all your recent articles: \n" + \
                "\n \n \n SOFTWARE ENGINEERING \n \n \n"

    for scraped_article in software_engineering_articles:
        email_body += f"{scraped_article.title} {scraped_article.link} \n"
    
    return email_body