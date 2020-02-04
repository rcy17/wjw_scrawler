"""
Here defines PointReporter, which send email from a given 163 email to respect email address

@Author : rcy17
@Date   : 2020/2/4
"""
from smtplib import SMTP_SSL

from .email_reporter import EmailReporter


class PointReporter(EmailReporter):
    def __init__(self, config_path='point.json', debug=False):
        super().__init__(config_path, debug)

    def process(self, messages):
        server = SMTP_SSL('smtp.163.com')
        server.ehlo()
        server.login(self.account['username'], self.account['password'])

        for province, items in messages.items():
            province_messages = [(name, msg['title'], f'{name}：<a href={msg["url"]}>{msg["title"]}</a>')
                                 for name, msg in items]
            receivers = self.receivers.get(province, self.receivers['default'])
            if not receivers:
                continue
            if isinstance(receivers, str):
                receivers = [receivers]
            for receiver in receivers:
                for source, subject, message in province_messages:
                    self.send_email(server, receiver, source, subject, message)
        server.close()
