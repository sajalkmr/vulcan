import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class MySpider(CrawlSpider):
name = 'myspider'
allowed_domains = ['example.com']
start_urls = ['https://example.com']

rules = (
    Rule(LinkExtractor(allow=['/blog/\d+/']), callback='parse_item', follow=False), 
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
            if name and value: 
                payload[name] = value 

        # SQL Injection
        if method == 'post' and self.is_vulnerable_sql(action, payload): 
            print('Vulnerable to SQL injection!') 

        # XSS
        if 'script alert(' in response.text: 
            print('Vulnerable to XSS!') 

        # RFI
        if 'include"' in response.text: 
            print('Vulnerable to RFI!') 
        
        # CSRF
        if 'csrf_token' not in payload and 'CSRF protection' not in response.text: 
            print('Vulnerable to CSRF!') 
        
        # Sensitive info disclosure
        if 'Password:' in response.text or 'Credit Card:' in response.text: 
            print('Sensitive information disclosed') 
        
        # PHP inclusion
        if '.php' in action:
            print('PHP file inclusion vulnerability')
        
        # Shell injection
        if '`' in ' '.join(payload.values()): 
            print('Shell injection vulnerability')
        
        # Broken access control 
        
        # SQL injection 
        if not any(esc in query for query in response.text for esc in ["'", '"', '%']): 
            print('Potential SQL injection') 
        
        # OS injection
        if any(os.system in response.text for os in ["exec", "worksjoin"]) or any(os in response.text for os in ["; ", "| "]): 
            print('OS injection vulnerability') 
        
        # Command injection
        if any( commands in response.text for commands in ["; ", "| "]): 
            print('Command injection vulnerability') 
        
        # Session issues 
        session_ids = [s['id'] for s in requests.utils.dict_from_cookiejar(self.cookies)]
        if len(session_ids) > len(set(session_ids)): 
            print('Session fixation vulnerability') 
        
        # Source code disclosure 
        
        # Backups disclosing sensitive info
        
        # And more...

def is_vulnerable_sql(self, url, payload): 
    # SQL Injection vulnerability logic