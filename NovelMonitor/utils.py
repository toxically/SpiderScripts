#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import *


def send_email(book_title, book_content):
    """
        邮件发送功能
    """
    msg = MIMEText(book_content, 'html', 'utf-8')

    msg['Subject'] = Header(book_title, 'utf-8')
    msg['From'] = Header('小说订阅', 'utf-8')
    msg['To'] = Header('Toxic', 'utf-8')

    try:
        smtp_obj = smtplib.SMTP(mail_config['MAIL_SMTP_HOST'], mail_config['MAIL_SMTP_PORT'])
        smtp_obj.login(mail_config['MAIL_USER'], mail_config['MAIL_PASSWORD'])
        smtp_obj.sendmail(mail_config['MAIL_USER'], mail_config['MAIL_RECEIVERS'], msg.as_string())
    except smtplib.SMTPException as e:
        print('小说{title}更新订阅邮件，发送失败！'.format(title=book_title))
