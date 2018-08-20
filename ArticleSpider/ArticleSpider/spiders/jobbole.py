# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']


    def parse(self, response):
        '''
        1、获取文章列表页中的文章URL并交给Scrapy下载好并进行解析
        2、获取下一页的URL并交给Scrapy进行下载，下载后交给Parse函数
        #获取当前域名的方法
        #response.url
        #拼接域名网址 对于场景url缺失主域名有很好的效果
        #parse.urljoin(response.url,post_url)
        '''
        #解析列表页中的所有文章URL并交给Scrapy下载后并进行解析
        #post_urls = response.xpath('//a[@class="archive-title"]/@href').extract()
        #front_image_urls = response.xpath('//div[@class="post-thumb"]/a/img/@src').extract()
        #获取文章缩略图及文章详情地址
        nodes = response.xpath('//div[@class="post floated-thumb"]/div[1]')
        for node in nodes:
            post_url = node.xpath('a/@href').extract_first()
            front_image_url = node.xpath('a/img/@src').extract_first()
            yield scrapy.Request(url = parse.urljoin(response.url,post_url), meta = {"front_image_url":parse.urljoin(response.url,front_image_url)},callback = self.parse_detail)
        
        # next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        # if next_url:
        #     yield scrapy.Request(url = parse.urljoin(response.url,next_url), callback = self.parse)
       
    
    def parse_detail(self, response): 
        #提取文章的具体字段
        #xpath N种方法
        #re_selector = response.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[1]/h1/text()')
        #re_selector2 = response.xpath('//*[@id="post-114253"]/div[1]/h1/text()')

        article_item = JobBoleArticleItem()

        #文章ID
        article_item['id'] = int(response.url.split('/')[-2])
        #封面
        front_image_url = response.meta.get('front_image_url','')
        article_item['front_image_url'] = [front_image_url]     #因为ImagesPipeline接收的值是一个数组 所以此处转换为数组
        #标题
        article_item['title'] = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        #创建时间
        article_item['create_date'] = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·', '').strip() 
        #文章分类
        article_item['article_type'] = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()[0].strip() 
        #关键字
        keyword_lists = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()[1:]
        keyword = ''
        for key in keyword_lists:
            keyword = keyword+key+','
        article_item['keyword'] = keyword[:-1]

        #点赞数
        thumbup_num = response.xpath('//div[@class="post-adds"]/span[1]/h10/text()').extract()[0]
        if thumbup_num == '':
            thumbup_num = 0
        else:
            thumbup_num = int(thumbup_num)
        article_item['thumbup_num'] = thumbup_num
        #收藏数
        collection_num = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract()[0].replace('收藏', '').strip() 
        if collection_num == '':
            collection_num = 0
        else:
            collection_num = int(collection_num)
        article_item['collection_num'] = collection_num
        #文章内容
        article_item['content'] = response.xpath('//div[@class="entry"]').extract()[0]

        yield article_item




       