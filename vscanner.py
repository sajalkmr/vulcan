import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import requests

class MySpider(CrawlSpider):
    name = 'myspider'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            method = form.get('method')
            inputs = form.find_all('input')
            payload = {}
            for input in inputs:
                name = input.get('name')
                value = input.get('value')
                if name:
                    payload[name] = value
            if method == 'post':
                response = requests.post(action, data=payload)
            else:
                response = requests.get(action, params=payload)
            if 'SQL syntax' in response.text:
                print('Vulnerable to SQL injection')
            if '<script>alert' in response.text:
                print('Vulnerable to XSS')
            if 'include' in response.text:
                print('Vulnerable to RFI')