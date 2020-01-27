"""
Entry

@Author : rcy17
@Date   : 2020/1/27
"""
import time

from crawler.manager import Manger
import reporter

DEBUG = True


def main():
    manager = Manger(processor=reporter.PrintReporter(debug=DEBUG), debug=DEBUG)
    manager.load_config_info()
    while True:
        # once per minute
        cost_time = manager.run()
        if cost_time < 60:
            time.sleep(60 - cost_time)


if __name__ == '__main__':
    main()
