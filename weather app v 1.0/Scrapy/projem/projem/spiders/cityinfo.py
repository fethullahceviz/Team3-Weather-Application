from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
import psycopg2
import scrapy

connection  = psycopg2.connect(host='localhost', user='postgres', password=#enterpass, dbname=#enterdabasename)
cur         = connection.cursor()

cur.execute(""" CREATE TABLE IF NOT EXISTS city_info ( 
                city text NOT NULL, 
                land text NOT NULL, 
                province text NOT NULL, 
                population integer NOT NULL) """)
connection.commit()

class Weather1(scrapy.Spider):
    name = 'weather'
    start_urls = ['https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27deki_illerin_n%C3%BCfuslar%C4%B1_(2020)']
    
    def parse(self, response):

        trrows = response.css('table.wikitable tr') 
        cur.execute("SELECT count(city) FROM city_info WHERE land='Turkey';")
        trcitycount=cur.fetchone()[0]
        #print(citycount)

        if trcitycount==0:
            for row in trrows[1:]:

                city_name    = row.xpath('td[1]/a/text()').get()
                population_  = row.xpath('td[2]/text()').get() 
                province_    = row.xpath('td[3]/a/text()').get()
                #print("----",city_name,population_,province_,"----")
                if  province_   == None:                
                    province_   = row.xpath('td[3]/text()').get()                   	
            
                cur.execute("INSERT INTO city_info (land, city, province, population) VALUES (%s, %s, %s, %s)",("Turkey", city_name, province_, population_))
                connection.commit()
        else:
            print("Cities are already saved")

class Weather2(scrapy.Spider):
    name = 'weather'
    start_urls = ['https://nl.wikipedia.org/wiki/Lijst_van_grootste_gemeenten_in_Nederland']
        
    def parse(self, response):

        nlrows = response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr')

        cur.execute("SELECT count(city) FROM city_info WHERE land='Netherland';")
        nlcitycount=cur.fetchone()[0]

        if nlcitycount==0:

            for row in nlrows[1:]:

                city_name    = row.xpath('td[2]/span[2]/span/a[2]/text()').get()   
                #print(city_name)
                province_    = row.xpath('td[3]/span[2]/span/a[2]/text()').get()
                #print(province_)  
                population_  = row.xpath('td[4]/b/text()').get().strip().replace(".","") 
                #print(population_)     
                #print("----------------------------------------")    

                cur.execute("INSERT INTO city_info(land,city,province,population) VALUES(%s,%s,%s,%s)",("Netherland",city_name, province_, population_))
                connection.commit()
        else:
            print("Cities are already saved")
                
class Weather3(scrapy.Spider):
    name = 'weather'
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    def parse(self, response):
        usarows = response.xpath('//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr')  
        #print(rows)
        cur.execute("SELECT count(city) FROM city_info WHERE land='Usa';")
        usacitycount=cur.fetchone()[0]

        if usacitycount==0:
            for row in usarows[1:]:

                city_name    = row.xpath('td[1]/a/text()').get()               
                if city_name==None:
                    city_name    = row.xpath('td[1]/i/a/text()').get()
                    if city_name==None:
                        city_name    = row.xpath('td[1]/i/b/a/text()').get()
                        if city_name==None:
                            city_name    = row.xpath('td[1]/b/a/text()').get()
                            if city_name==None:
                                city_name    = row.xpath('td[1]/b/a/i/text()').get()

                #print(city_name)
                province_    = row.xpath('td[2]/a/text()').get()
                #print(province_)  
                population_  = row.xpath('td[3]/text()').get().strip().replace(",","")          
                #print(population_)     
                #print("----------------------------------------")               

                cur.execute("INSERT INTO city_info(land,city,province,population) VALUES(%s,%s,%s,%s)",("Usa",city_name, province_, population_))
                connection.commit()
        else:
            print("Cities are already saved")

configure_logging()
settings = get_project_settings()
runner   = CrawlerRunner(settings)

@defer.inlineCallbacks

def crawl():
    yield runner.crawl(Weather1)
    yield runner.crawl(Weather2)
    yield runner.crawl(Weather3)
    reactor.stop()

crawl()
reactor.run()

