"""
Entry

@Author : rcy17
@Date   : 2020/1/27
"""
import time
from json import load
from pathlib import Path

from crawler.manager import Manger


def process_messages(messages):
    """
    Here we get all updated messages and report them
    Now report method hasn't finished yet, just print it
    Maybe we can consider using SMTP or wechat bot

    :param messages: {<name:str>: [{'title': <title:str>, 'url': <url:str>}, ...], ...}
    :return: None
    """
    print('new messages:', messages)


def load_config_info(path='config'):
    directory = Path(path)
    config = {}
    if not directory.is_dir():
        raise NotADirectoryError(str(path) + ' is not a directory')
    for path in directory.iterdir():
        if path.suffix != '.json':
            continue
        try:
            config.update(load(open(str(path), 'r')))
        except Exception as e:
            print(f'Failed to load {str(path)}:', e)
    return config


def main():
    manager = Manger(processor=process_messages)
    config = load_config_info()
    for each in config.values():
        manager.add_crawler(each)
    while True:
        # once per minute
        cost_time = manager.run()
        time.sleep(60 - cost_time)


if __name__ == '__main__':
    main()
