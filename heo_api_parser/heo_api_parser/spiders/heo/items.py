# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class HeoItem(scrapy.Item):
    title = Field()
    id = Field()
    product_type = Field()
    dbId = Field()
    categories = Field()
    state_info = Field()
    evp = Field()
    barcode = Field()
    weight = Field()

    price = Field()

    es_description = Field()
    es_name = Field()

    en_description = Field()
    en_name = Field()

    images = Field()

    raw_json = Field()
