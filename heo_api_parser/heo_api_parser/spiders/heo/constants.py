import os
class URL:
    articles_by_type_url = 'https://www.heo.com/api/articlesByType'
    articles_url = 'https://www.heo.com/api/articles'
    product_url = 'https://www.heo.com/de/es/product/{id}'
    login_url = 'https://www.heo.com/auth/login'
    main_url = 'https://www.heo.com/de/es'

class PAYLOAD:
    articles_payload = '{{"searchParams":"{search_param}","search":["advforrealms"],"offset":0,"limit":200,"language":"es","overview":false}}'
    article_section_payload = '{{"searchParams":"{search_param}","offset":{offset},"limit":200,"language":"es","overview":false}}'
    login_payload = '{{"name":"{mail}","password":"{password}","stayConnected":true}}'

class AUTH:
    mail = os.environ['mail']
    password = os.environ['password']