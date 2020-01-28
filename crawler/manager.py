"""
A Manager class to manager crawler for different provinces

@Author : rcy17
@Date   : 2020/1/27
"""
import asyncio
from pathlib import Path
from datetime import datetime
from json import load

from aiohttp import ClientSession

from .crawler import Crawler

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.35 (KHTML, like Gecko)'
                  ' Chrome/79.0.3945.130 Safari/537.35',
    'Cookie': '',
}

# Notice that this Cookie should be set yourself from http://wsjkw.sh.gov.cn/xwfb/index.html
HEADERS['Cookie'] += 'zh_choose=s; zh_choose=s; yd_cookie=c6baceba-b902-468bc47e68e15355c176d0fed500f6ead6e7; _ydclearance=4d5498cd30d9c8426d9a5e41-ca53-4569-9ce3-b41bbaa02723-1580227445; AlteonP=AO1GZGHbHKydo9ENLQrXeA$$'


class Manger:
    def __init__(self, path='records', processor=None, debug=False):
        self._crawlers = {}
        self._path = Path(path)
        self._path.mkdir(parents=True, exist_ok=True)
        self._processor = processor
        self._messages = {}
        self.debug = debug

    def load_config_info(self, path='config'):
        """Load xxx.json config to config crawlers"""
        directory = Path(path)
        config = []
        if not directory.is_dir():
            raise NotADirectoryError(str(path) + ' is not a directory')
        for path in directory.iterdir():
            if path.suffix != '.json':
                continue
            try:
                self.add_crawler(load(open(str(path), 'r')))
            except Exception as e:
                print(f'Failed to load {str(path)}:', e)
        return config

    def add_crawler(self, info):
        info['path'] = self._path.joinpath(info.get('name', info['url'][-5:]) + '.json')
        self._crawlers[info['name']] = Crawler(manager=self, **info)

    async def run_crawlers(self):
        async with ClientSession(headers=HEADERS) as session:
            tasks = [crawler.get_task(session) for crawler in self._crawlers.values()]
            result = await asyncio.gather(*tasks, return_exceptions=True)
            for index, msg in enumerate(result):
                if isinstance(msg, Exception):
                    print(f'[{datetime.now()}][ERROR] {type(msg)}: {msg}')

    def run(self):
        """Run the pipeline"""
        start_time = datetime.now()
        self._messages.clear()
        loop = asyncio.get_event_loop()
        try:
            start = datetime.now()
            loop.run_until_complete(self.run_crawlers())
            stop = datetime.now()
            if self.debug:
                print(f'[{datetime.now()}] All crawlers cost', (stop-start).total_seconds(), 'seconds')
        except Exception as e:
            print(e)
        self._processor(self._messages)
        stop_time = datetime.now()
        return (stop_time - start_time).total_seconds()

    def need_report(self, title):
        """Judge if the news should be reported"""
        keys = ['新型冠状病毒感染的肺炎', '最新疫情通报']
        for key in keys:
            if key in title:
                return True
        # This is just for Hainan
        if '确诊' in title and '例' in title:
            return True
        if self.debug:
            print('Ignore title:', title)
        return False

    def add_message(self, source, message):
        """Try to add new message to report"""
        if not self.need_report(message['title']):
            return False
        # Now we just have one message, but maybe we will extend it in future, so use list
        self._messages.setdefault(source, [])
        self._messages[source].append(message)
        return True



