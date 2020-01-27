"""
Here defines BasicReporter, which is an abstract class

@Author : rcy17
@Date   : 2020/1/27
"""


class BasicReporter:
    def __call__(self, messages):
        return self.process(messages)

    def process(self, messages):
        """
        Report updated messages

        :param messages: {<name:str>: {["url": <url:str>, "title": <title:str>], ...}, ...}
        :return:
        """
        raise NotImplementedError

