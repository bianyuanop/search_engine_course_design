# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import sqlite3
import requests
from itemadapter import ItemAdapter
# from stemmingor import Stemmingor
from stemmingor import Stemmingor

DB_LOCATION = '/home/chan/workspace/searchEng2/data.db'
STORAGE = '/home/chan/workspace/searchEng2/storage'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

class SpiderPipeline:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_LOCATION)
        self.cursor = self.conn.cursor()
        self.cn_stemminor = Stemmingor(mode='cn')
        self.en_stemminor = Stemmingor(mode='en')

    def close_spider(self, spider):
        self.conn.close()

    def insert_item(self, item):
        self.cursor.execute('''
        INSERT INTO data (filename, url, words_file)
        VALUES (?, ?, ?)
        ''', (item['filename'],item['url'], item['words_file']))
        self.conn.commit()
    
    def exists(self, url):
        cur = self.cursor.execute("SELECT * FROM data WHERE url = ?", (url,))
        return cur.fetchone() is not None
    
    def validate(self, item):
        href = item['href'] 
        item_basename = href.replace('/','_')
        if href.startswith('//'):
            url = 'https:' + href
            item['url'] = url

        elif href.startswith('http://') \
            or href.startswith('https://'):
            item['url'] = href

        else:
            url = 'https://' + item['base_site'] + '/' + href.lstrip('/')
            item['url'] = url
        
        words_file = item_basename + '.txt'
        filename = item_basename + '.html'

        item['filename'] = filename
        item['words_file'] = words_file
    
    def process_cn(self, item):
        file_path = os.path.join(STORAGE, item['filename'])
        words_file_path = os.path.join(STORAGE, item['words_file'])

        resp = requests.get(item['url'], headers=HEADERS)
        html = resp.text
        words = self.cn_stemminor.stem_raw_html(html)
        
        with open(words_file_path, 'w') as f:
            f.write(' '.join(words))
        
        with open(file_path, 'w') as f:
            f.write(resp.text)

    def process_en(self, item):
        file_path = os.path.join(STORAGE, item['filename'])
        words_file_path = os.path.join(STORAGE, item['words_file'])

        resp = requests.get(item['url'], headers=HEADERS)
        html = resp.text
        words = self.en_stemminor.stem_raw_html(html)
        
        with open(words_file_path, 'w') as f:
            f.write(' '.join(words))
        
        with open(file_path, 'w') as f:
            f.write(resp.text)

    def process_item(self, item, spider):
        if self.exists(item['href']):
            pass
        else:
            self.validate(item)
            if 'stackoverflow' in item['base_site']:
                self.process_en(item)
                self.insert_item(item)

            if 'bilibili' in item['base_site']:
                self.process_cn(item)
                self.insert_item(item)

        return item

if __name__ == '__main__':
    item = {
        'base_site': 'stackoverflow.com',
        'filename': '_questions_71855183_how-to-read-a-json-file-and-put-it-into-multiple-array-without-knowing-the-key-i.html',
        'href': '/questions/71855183/how-to-read-a-json-file-and-put-it-into-multiple-array-without-knowing-the-key-i',
        'title': 'How to read a json file and put it into multiple array without knowing the key in JavaScript',
        'url': 'https://stackoverflow.com/questions/71855183/how-to-read-a-json-file-and-put-it-into-multiple-array-without-knowing-the-key-i', 'words_file': '_questions_71855183_how-to-read-a-json-file-and-put-it-into-multiple-array-without-knowing-the-key-i.txt'
    }

    item2 = {
        'base_site': 'bilibili.com',
        'href': '//www.bilibili.com/read/cv16123865?from=articleDetail',
        'title': '涩涩允许！！！#149'
    }

    pipeline = SpiderPipeline()
    print(pipeline.process_item(item, None))
    print(pipeline.process_item(item2, None))