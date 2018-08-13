# -*- coding: utf-8 -*-
import scrapy
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']


    def parse(self, response):
        '''
        1、获取文章列表页中的文章URL并交给Scrapy下载好并进行解析
        2、获取下一页的URL并交给Scrapy进行下载，下载后交给Parse函数
        '''

        #解析列表页中的所有文章URL并交给Scrapy下载后并进行解析
        #获取当前域名的方法
        #response.url
        post_urls = response.xpath('//a[@class="archive-title"]/@href').extract()
        for post_url in post_urls:
            yield scrapy.Request(url = parse.urljoin(response.url,post_url), callback = self.parse_detail)

        #提取下一页并交给Scrapy下载
        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url = parse.urljoin(response.url,next_url), callback = self.parse)


    def parse_detail(self, response): 
        #提取文章的具体字段
        #xpath N种方法
        #re_selector = response.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[1]/h1/text()')
        #re_selector2 = response.xpath('//*[@id="post-114253"]/div[1]/h1/text()')
        #标题
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        #创建时间
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·', '').strip() 
        #文章分类
        article_type = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()[0].strip() 
        #关键字
        keyword_lists = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()[1:]
        keyword = ''
        for key in keyword_lists:
            keyword = keyword+key+','
        keyword = keyword[:-1]

        #点赞数
        thumbup_num = response.xpath('//div[@class="post-adds"]/span[1]/h10/text()').extract()[0]
        if thumbup_num == '':
            thumbup_num = 0
        else:
            thumbup_num = int(thumbup_num)
        #收藏数
        collection_num = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract()[0].replace('收藏', '').strip() 
        if collection_num == '':
            collection_num = 0
        else:
            collection_num = int(collection_num)
        #文章内容
        content = response.xpath('//div[@class="entry"]').extract()[0]
        pass
