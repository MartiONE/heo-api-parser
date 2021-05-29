from scrapy import Request, Spider
from heo_api_parser.items import HeoItem
from copy import deepcopy
import json

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.heo.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.heo.com/de/es/',
    'Accept-Language': 'en-US,en;q=0.9',
}

articles_by_type_url = 'https://www.heo.com/api/articlesByType'
articles_url = 'https://www.heo.com/api/articles'
product_url = 'https://www.heo.com/de/es/product/{id}'

articles_payload = '{{"searchParams":"{search_param}","search":["advforrealms"],"offset":0,"limit":200,"language":"es","overview":false}}'
article_section_payload = '{{"searchParams":"{search_param}","offset":{offset},"limit":200,"language":"es","overview":false}}'

search_params = {
    'games': 'C8689_O1',
    'toys': 'C8657_O1',
    'collection_articles': 'C8661_O1',
    'clothing': 'C866b_O1',
    'home_gifts': 'C8675_O1',
    'anime_manga': 'C867f_O1'
}

class HeoSpider(Spider):
    name = "heo"

    def start_requests(self):
        # Gather cookies
        yield Request('https://www.heo.com/de/es', callback=self.parse)

    def parse(self, response):
        for section, search_param in search_params.items():
            meta = {'section': section,
                    'search_param': search_param,
                    'page': 1,
                    'offset': 0}
            payload = article_section_payload.format(**meta)
            yield response.follow(articles_url, headers=headers, body=payload, method='POST',
                                  callback=self.parse_article_listing, meta=meta)
    
    def parse_article_listing(self, response):
        json_response = json.loads(response.text)

        if response.meta['page'] == 1:
            yield from self.generate_pagination_urls(response, json_response)

        for article in json_response['articles']:
            item = HeoItem()

            item['title'] = article['localization']['enName']
            item['id'] = article['articleNumber']
            item['dbId'] = article['productTypes'][0]['dbId']
            item['categories'] = article['categorisation']
            item['state_info'] = article['stateInformation']
            item['evp'] = article['information'][0]['evp']
            item['barcode'] = article['information'][0]['barcodes']
            item['weight'] = article['information'][0]['weight']

            item['price'] = 'placeholder'
            
            item['es_description'] = article['localization']['esDescription']
            item['es_name'] = article['localization']['esName']

            item['en_description'] = article['localization']['enDescription']
            item['en_name'] = article['localization']['enName']

            item['images'] = self.extract_images(article)

            item['raw_json'] = article

            yield item
    
    def generate_pagination_urls(self, response, json_response):
        hits = json_response['hits']
        num_pages = (int(hits) // 200) + 2
        self.logger.info(f'Detected {num_pages} in section {response.meta["section"]}')
        for page in range(2, num_pages):
            new_meta = deepcopy(response.meta)
            new_meta['page'] = page
            new_meta['offset'] = 200 * (page-1)
            payload = article_section_payload.format(**new_meta)
            yield response.follow(articles_url, headers=headers, body=payload, method='POST',
                                  callback=self.parse_article_listing, meta=new_meta)
    

    def extract_images(self, article):
        images = []
        for i, section in article['images'].items():
            if i == 'preview':
                images.append(f'https://www.heomedia.com/{section["path"]}{section["file"]}')
            elif i == 'main':
                for subsection in section.values():
                    images.append(f'https://www.heomedia.com/{subsection["path"]}{subsection["file"]}')
        return images

