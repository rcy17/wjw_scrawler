"""
Here defines EmailReporter, which send email from a given 163 email

@Author : rcy17
@Date   : 2020/1/27
"""
from json import load
from getpass import getpass
from datetime import datetime
from smtplib import SMTP
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
        server = SMTP('smtp.163.com')
        server.login(self.account['username'], self.account['password'])
        message = '<br>'.join(f'{index}. {name}: <a href={msg["url"]}>{msg["title"]}</a>'
                              for index, (name, [msg]) in enumerate(messages.items()))
        for receiver in self.receivers:
            try:
                msg = MIMEMultipart()
                msg['From'] = self.account['username']
                msg['To'] = receiver
                msg['Subject'] = '卫健委新闻更新'
                # msg.set_content(message)
                content = MIMEText(message, 'html', 'utf-8')
                msg.attach(content)
                server.send_message(msg)
                print(f'[{datetime.now()}] Succeed to send email to {receiver}')
            except Exception as e:
                print(f'[{datetime.now()}] Failed to send email to {receiver}:', type(e), e)
        server.close()
