import sys
import scrapy
from fake_useragent import UserAgent

ua = UserAgent()

def err_handler(err):
    print ("Exception has occured:", err)
    print ("Exception type:", type(err))

    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno
    print ("\nERROR:", err, "on line number:", line_num)
    print ("traceback:", traceback, "-- type:", err_type)

class WhiskyspiderSpider(scrapy.Spider):
    name = 'whiskyspider'
    allowed_domains = ['whiskyshop.com']
    user_agent = ua.random
    #start_urls = ['https://www.whiskyshop.com/scotch-whisky/all?item_availability=In+Stock']
   
    def start_requests(self):
        try:
            # make playwright load the page, give it the url, 
            # send the response back to scrapy
            header = {'user-agent': ua.random,
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "max-age=0",
                "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1"
            }
            
            meta = dict(
                playwright = True,
                playwright_include_page = True, # creates a page pbject to work with
                handle_httpstatus_all = True # ??
            )
            yield scrapy.Request('https://www.whiskyshop.com/scotch-whisky/all?item_availability=In+Stock',meta=meta, headers=header, 
                        callback=self.parse)

        except Exception as err:
            err_handler(err)

    def parse(self, response):

        try:
            #products = response.css('div.product-item-info')
            for item in response.css('div.product-item-info'):
                try:
                    yield{
                        'link' : item.css('a.product-item-link::attr(href)').get(),
                        'title' : item.css('a.product-item-link::text').get(),
                        'price' : item.css('span.price::text').get().replace('£', '')
                    }
                except:
                    yield{
                        'link' : item.css('a.product-item-link::attr(href)').get(),
                        'title' : item.css('a.product-item-link::text').get(),
                        'price' : 'Sold out'
                    }

            next_page = response.css('a.action.next::attr(href)').get()
            if next_page is not None:        
                yield scrapy.Request(url=next_page, meta=response.meta,  headers=response.header, callback=self.parse)

        except Exception as err:
            err_handler(err)