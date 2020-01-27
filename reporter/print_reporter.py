"""
Here defines PrintReport, which just print info to stdout

@Author : rcy17
@Date   : 2020/1/27
"""
from datetime import datetime

from .basic_reporter import BasicReporter


class PrintReporter(BasicReporter):
    def __init__(self, **kwargs):
        pass

    def process(self, messages):
        print(f'[{datetime.now()}] get {len(messages)} new messages:{messages}')

