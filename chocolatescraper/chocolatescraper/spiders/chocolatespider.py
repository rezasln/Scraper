import scrapy
from chocolatescraper.items import ChocolateProduct
from urllib.parse import urlencode
from chocolatescraper.apikey import API_KEY


def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class ChocolatespiderSpider(scrapy.Spider):

    name = "chocolatespider"
    
    def start_requests(self):
        start_url = 'https://www.chocolate.co.uk/collections/all'
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)

    def parse(self, response):

        products = response.css("product-item")

        product_item = ChocolateProduct()

        for product in products:
            
            if '<span class=\"price price--highlight\">\n              <span class=\"visually-hidden\">Sale price' in product.css('span.price').get():
                price = product.css('span.price').get().replace('<span class=\"price price--highlight\">\n              <span class=\"visually-hidden\">Sale price','').replace('</span>','').replace("\n", "")
            else:
                 price = product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>','').replace("\n", "")
        
            product_item['name'] = product.css('a.product-item-meta__title::text').get()
            product_item['price'] = price
            product_item['url'] = "https://www.chocolate.co.uk" + product.css('div.product-item-meta a').attrib['href']
            yield product_item
            
        
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(next_page_url, callback=self.parse)
