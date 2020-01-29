"""
Program entry

@Author : rcy17
@Date   : 2020/1/27
"""
import time

from crawler.manager import Manger
import reporter

DEBUG = True
INTERVAL_SECOND = 120


def main():
    manager = Manger(processor=reporter.EmailReporter(debug=DEBUG), debug=DEBUG)
    manager.load_config_info()
    while True:
        # once per minute
        cost_time = manager.run()
        if cost_time < INTERVAL_SECOND:
            time.sleep(INTERVAL_SECOND - cost_time)


if __name__ == '__main__':
    main()
