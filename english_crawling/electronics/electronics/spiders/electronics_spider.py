import scrapy
from electronics.items import ElectronicsItem

class ElectronicsSpider(scrapy.Spider):
    name = "electronics"

    def start_requests(self):
        base_url = 'https://www.electronicsweekly.com/page/'
        search_option = '/?s=kaist'
        for i in range(2):
            page_num = i + 1
            url = base_url + str(page_num) + search_option
            yield scrapy.Request(url, self.parse, dont_filter = True)

    def parse(self, response):
        url_list = response.xpath('//*[@class="post-listing "]/article/h2/a/@href').extract()
        for url in url_list:
            article_url = url
            yield scrapy.Request(article_url, self.parse_article, meta={'url' : article_url})
    
    def parse_article(self, response):

        item = ElectronicsItem()
        
        article_url = response.meta['url']
        article_title = response.xpath('//*[@itemprop="name"]/text()').extract()[0]
        article_title = article_title.strip()
        article_data = ''.join(response.xpath('//*[@class="entry"]/p/text()').extract())
        article_data = article_data.replace('\n', '')
        article_data = article_data.replace('\r', '')

        item['urls'] = article_url
        item['titles'] = article_title
        item['contents'] = article_data


        yield item