"""
A Basic Crawler class to crawl a web

@Author : rcy17
@Date   : 2020/1/27
"""
import asyncio
from functools import reduce
from json import load, dump
from sys import stderr

from bs4 import BeautifulSoup
from aiohttp import ClientSession
from chardet import detect

from crawler import parser

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/79.0.3945.130 Safari/537.36',
    'Cookie': '',
}

# Notice that this Cookie should be set yourself from http://wsjkw.sh.gov.cn/xwfb/index.html
HEADERS['Cookie'] += 'zh_choose=s; zh_choose=s; yd_cookie=c6baceba-b902-468bc47e68e15355c176d0fed500f6ead6e7; _ydclearance=7b9b8e13af671ad0e01df357-c6c7-4109-ad21-b5dd69430036-1580217707; AlteonP=AHeRLWHbHKzz4HoGUzT+Nw$$'


class Crawler:
    def __init__(self, manager, url, search_path, name, path, parser_name=None, **kwargs):
        self.manager = manager
        self.url = url
        self.search_path = search_path
        self.name = name
        self.path = path
        self.parser = parser_name
        self.others = kwargs
        try:
            self.record = load(open(self.path, 'r', encoding='utf-8'))
        except FileNotFoundError:
            self.record = {}

    async def run(self):
        async with ClientSession(headers=HEADERS) as session:
            try:
                async with session.get(self.url, timeout=30, verify_ssl=False) as response:
                    # get data first
                    data = await response.read()
            except Exception as e:
                print('[ERROR]', type(e), e)
                return
        # Now serialize by Beautiful Soup with the given path

        soup = BeautifulSoup(data.decode(detect(data)['encoding']), 'lxml')
        try:
            node = reduce(lambda past, info: past.find(**info), self.search_path, soup)
        except AttributeError:
            print('[CRITICAL] Fail to serialize', self.url, file=stderr)
            return
        parse_function = getattr(parser, self.parser, None)
        if parse_function is None:
            print('[WARNING]', self.name, 'has no parser', file=stderr)
            return
        # Parse newest news title and url
        result = parse_function(self.url, node)

        record_title = self.record.get('title')
        if result['title'] == record_title:
            return
        # If this is not recorded, save and report it
        self.record = result
        dump(result, open(self.path, 'w', encoding='utf-8'), ensure_ascii=False)
        self.manager.add_message(self.name, result)

    def get_task(self):
        return asyncio.ensure_future(self.run())
