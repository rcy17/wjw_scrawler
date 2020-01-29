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
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.34 (KHTML, like Gecko)'
                  ' Chrome/79.0.3945.130 Safari/537.34',
}


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
        try:
            start = datetime.now()
            asyncio.run(self.run_crawlers())
            stop = datetime.now()
            if self.debug:
                print(f'[{datetime.now()}] All crawlers cost', (stop-start).total_seconds(), 'seconds')
        except Exception as e:
            print(e)
        self._processor(self._messages)
        stop_time = datetime.now()
        return (stop_time - start_time).total_seconds()

    def need_report(self, source, title):
        """Judge if the news should be reported"""
        need = False
        keys = ['新型冠状病毒感染的肺炎疫情', '最新疫情通报']
        for key in keys:
            if key in title:
                need = True
        if ('确诊' in title or '新增' in title) and '例' in title:
            need = True
        trash = ['工作', '寻找', '应急', '原则']
        for key in trash:
            if key in title:
                need = False
        if self.debug and not need:
            print(f'Ignore title from {source}: {title}')
        return need

    def add_message(self, source, message):
        """Try to add new message to report"""
        if not self.need_report(source, message['title']):
            return False
        # Now we just have one message, but maybe we will extend it in future, so use list
        self._messages.setdefault(source, [])
        self._messages[source].append(message)
        return True



