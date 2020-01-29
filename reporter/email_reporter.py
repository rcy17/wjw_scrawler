"""
Here defines EmailReporter, which send email from a given 163 email

@Author : rcy17
@Date   : 2020/1/27
"""
from json import load
from getpass import getpass
from datetime import datetime
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .basic_reporter import BasicReporter


class EmailReporter(BasicReporter):
    def __init__(self, config_path='email.json', debug=False):
        config = load(open(config_path))
        account = config.get('from', {})
        if not account.get('username'):
            account['username'] = input('please input email full username:')
            account['password'] = ""
        if not account.get('password'):
            account['password'] = getpass('please input password')
        self.account = account
        # It must exist, or this reporter is senseless
        self.receivers = config['to']

    def process(self, messages):
        server = SMTP_SSL('smtp.163.com')
        server.ehlo()
        server.login(self.account['username'], self.account['password'])
        messages = [(name, msg['title'], f'{name}: <a href={msg["url"]}>{msg["title"]}</a>')
                    for (name, [msg]) in messages.items()]
        '''message = '<br>'.join(f'{index + 1}. {name}: <a href={msg["url"]}>{msg["title"]}</a>'
                              for index, (name, [msg]) in enumerate(messages.items()))'''
        for receiver in self.receivers:
            for source, subject, message in messages:
                try:
                    # construct a html message
                    msg = MIMEMultipart()
                    msg['From'] = self.account['username']
                    msg['To'] = receiver
                    msg['Subject'] = source + '卫健委：' + subject
                    content = MIMEText(message, 'html', 'utf-8')
                    msg.attach(content)
                    server.send_message(msg)
                    print(f'[{datetime.now()}] Succeed to send email to {receiver}')
                except Exception as e:
                    print(f'[{datetime.now()}] Failed to send email to {receiver}:', type(e), e)
        server.close()
