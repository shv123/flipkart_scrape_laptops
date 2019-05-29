# -*- coding: utf-8 -*- 


import scrapy
import pickle

class FlipkartbotSpider(scrapy.Spider):
    
    """  The spider is run by the python file run.py from the command line. 
         Command line input should be of the form python run.py number_of_laptops pickle_directory  """
	
    name = 'flipkartbot'
    allowed_domains = ['flipkart.com']
    start_urls = ['https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_0_6&otracker1=AS_QueryStore_OrganicAutoSuggest_0_6&as-pos=0&as-type=RECENT&as-searchtext=loptop&page=1']
  
	
    def __init__(self, iparg1='',iparg2='', **kwargs):
        FlipkartbotSpider.num_laptops = int(iparg1)
        FlipkartbotSpider.destination = iparg2
        super().__init__(**kwargs)
	

	
    page_num = 1       
    """ page_num is the number of the current page being scraped """
   
    k = 1
    laptops_dict = {}  
    ''' Dictionary that will be populated with laptop details '''
	

    def parse(self, response):
		
        titles = response.css("._3wU53n::text").extract()
        ratings = response.css(".hGSR34::text").extract()
        prices = response.css("._1vC4OE._2rQ-NK::text").extract()
        num_per_page = len(titles)
        
		
        '''  Titles, ratings and prices are lists that contain the titles, ratings 
		      in stars and the costs of the laptops scraped from that webpage as indicated by page_num '''
		
        num_pages = FlipkartbotSpider.num_laptops//num_per_page + 1
 
        ''' num_pages is the total number of pages that must be scraped from www.flipkart.com/laptops  '''
		
        if FlipkartbotSpider.page_num == num_pages :
            for i in range(FlipkartbotSpider.num_laptops % num_per_page + 1 , num_per_page + 1):
                del titles[-1]
                del ratings[-1]
                del prices[-1]
		
		
        ''' Above loop deletes the extra entries scraped from the last page being scraped '''
        

        
        j = 0
        i = 1
	   
        if FlipkartbotSpider.page_num != num_pages :
            for i in range(1,num_per_page+1):
                FlipkartbotSpider.laptops_dict[str(FlipkartbotSpider.k)] = [titles[j],ratings[j],prices[j]]                
                FlipkartbotSpider.k = FlipkartbotSpider.k+1
                j = j+1	

        else :
            for i in range(1,FlipkartbotSpider.num_laptops % num_per_page + 1):
                FlipkartbotSpider.laptops_dict[str(FlipkartbotSpider.k)] = [titles[j],ratings[j],prices[j]]                
                FlipkartbotSpider.k = FlipkartbotSpider.k+1
                j = j+1		
		
        
        ''' Above loops populate the dictionary laptops_dict '''	
        yield FlipkartbotSpider.laptops_dict
        
        FlipkartbotSpider.page_num += 1
        next_page = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page=' + str(FlipkartbotSpider.page_num)
        
        ''' Update url to go to the next page '''
		
        if FlipkartbotSpider.page_num <= num_pages :
            yield response.follow(next_page, callback = self.parse)
			
        ''' Continue scraping '''
			
        #print(FlipkartbotSpider.laptops_dict)
		
        with open(FlipkartbotSpider.destination + '/pickle.dir', 'wb') as f:
            pickle.dump(FlipkartbotSpider.laptops_dict, f)
			
        ''' Pickle the dictionary to the file pickle.dir in the path specified in the command line '''