"""
A Manager class to manager crawler for different provinces

@Author : rcy17
@Date   : 2020/1/27
"""
import asyncio
from pathlib import Path
from datetime import datetime

from .crawler import Crawler


class Manger:
    def __init__(self, path='records', processor=None, debug=False):
        self._crawlers = {}
        self._path = Path(path)
        self._path.mkdir(parents=True, exist_ok=True)
        self._processor = processor
        self._messages = {}
        self.debug = debug

    def add_crawler(self, info):
        info['path'] = self._path.joinpath(info.get('name', info['url'][-5:]) + '.json')
        self._crawlers[info['name']] = Crawler(manager=self, **info)

    def run(self):
        start_time = datetime.now()
        self._messages.clear()
        tasks = [crawler.get_task() for crawler in self._crawlers.values()]
        loop = asyncio.get_event_loop()
        try:
            start = datetime.now()
            loop.run_until_complete(asyncio.gather(*tasks))
            stop = datetime.now()
            if self.debug:
                print('All crawlers cost', (stop-start).total_seconds(), 'seconds')
        except Exception as e:
            print(e)
        self._processor(self._messages)
        stop_time = datetime.now()
        return (stop_time - start_time).total_seconds()

    def need_report(self, title):
        """Judge if the news should be reported"""
        keys = ['肺炎', '新增', '例', '病毒', '疫情']
        for key in keys:
            if key in title:
                return True
        if self.debug:
            print('Ignore title:', title)
        return False

    def add_message(self, source, message):
        if not self.need_report(message['title']):
            return False
        # Now we just have one message, but maybe we will extend it in future, so use list
        self._messages.setdefault(source, [])
        self._messages[source].append(message)
        return True



