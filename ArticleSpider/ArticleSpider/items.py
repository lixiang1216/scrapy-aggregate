# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    create_date = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    article_type = scrapy.Field()
    keyword = scrapy.Field()
    thumbup_num = scrapy.Field()
    collection_num = scrapy.Field()
    content = scrapy.Field()

