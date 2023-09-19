# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
import re
from bs4 import BeautifulSoup

# get settings
settings = get_project_settings()

# class
class KSUSpider(CrawlSpider):
    name = 'kennesaw.edu'
    allowed_domains = ['kennesaw.edu']
    start_urls = ['http://www.kennesaw.edu']

    # custom link extractor rule to ensure that only domain 'kennesaw.edu' allowed
    rules = (
        Rule(LinkExtractor(allow_domains='kennesaw.edu'), callback='parse_item', follow=True),
    )

    # use the user-agent setting in spider to let webserver know
    # download delay settings to not overload website
    # depth priority set to 1 so that we search in BFS and not DFS
    custom_settings = {
        'USER_AGENT': settings.get('USER_AGENT'),
        'DOWNLOAD_DELAY': 2,
        'DEPTH_PRIORITY': 1

        }

    # parse function to get the information and write dictionary entries
    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])

        # exctract information from response
        entry['pageid'] = response.url.split('/')[-1]
        entry['url'] = response.url
        entry['title'] = response.css('title::text').get()

        # extract text from the body element
        body_text = soup.body.get_text()

        # remove newlines and white spaces
        cleaned_body = ' '.join(body_text.split())


        entry['body'] = cleaned_body
        email_regular_expressions = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        entry['emails'] = re.findall(email_regular_expressions, response.text)

        yield entry
