"""
A Basic Crawler class to crawl a web

@Author : rcy17
@Date   : 2020/1/27
"""
import asyncio
from functools import reduce
from json import load, dump
from sys import stderr
from re import search

from bs4 import BeautifulSoup

from crawler import parser
from js2py import eval_js


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

    async def anti_anti_spider_for_shanghai(self, session, url, data):
        """
        This part is to fight with the anti_spider code of shanghai web
        """
        # parse parameter and function of JavaScript code
        param, func = search(r'(\d+).*?(function.*})', data).groups()
        # return string instead of eval it
        func = func.replace('eval("qo=eval;qo(po);")', 'return po')
        # now eval JavaScript and parse cookie
        func = eval_js(func)
        cookie = search(r"'(.*)'", func(param)).group(1)
        # now get again with our new cookie
        async with session.get(url, timeout=15, verify_ssl=False, headers={'Cookie': cookie}) as response:
            return await response.text()

    async def run(self, session):
        try:
            async with session.get(self.url, timeout=15, verify_ssl=False) as response:
                data, code = await response.text(), response.status
            # this part is for Shanghai specially
        except Exception as e:
            print('[ERROR]', self.name, type(e), e)
            return
        if code == 521:
            try:
                data = await self.anti_anti_spider_for_shanghai(session, self.url, data)
            except Exception as e:
                print('[ERROR]', self.name, type(e), e)
                return
        # Now serialize by Beautiful Soup with the given path
        soup = BeautifulSoup(data, 'lxml')
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
        self.manager.add_message(self.others['Chinese_name'], result)

    def get_task(self, session):
        return asyncio.ensure_future(self.run(session))
