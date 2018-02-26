#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import requests
from config import *
from utils import *
from lxml import etree
from dateutil.parser import parse

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'm.biquke.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
}


def check_update():
    for book_title, book_chapters_url in NOVELS:

        # 小说目录url转换成移动端url
        book_chapters_url = book_chapters_url.replace('www.biquke.com', 'm.biquke.com')

        r = requests.get(book_chapters_url, headers=headers)
        r.encoding = 'utf-8'
        r.raise_for_status()

        last_modified_time = r.headers.get('last-modified')

        time_delta = (datetime.datetime.now() - parse(last_modified_time).replace(
            tzinfo=None)).total_seconds() / 60 / 60

        if time_delta < 1:
            dom = etree.HTML(r.text)

            new_chapter_title = ''.join(dom.xpath('.//ul[@class="chapter"][1]/li[1]/a/text()'))
            new_chapter_url = 'http://m.biquke.com' + ''.join(dom.xpath('.//ul[@class="chapter"][1]/li[1]/a/@href'))

            # 获取更新章节的内容
            new_chapter_content = get_book_chapter_content(new_chapter_url)

            # 发送邮件
            email_title = '{book_title}-{book_chapter}'.format(book_title=book_title, book_chapter=new_chapter_title)
            send_email(email_title, new_chapter_content)
        time.sleep(5)


def get_book_chapter_content(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    response.raise_for_status()

    sel = etree.HTML(response.text)
    _chapter_content = sel.xpath('.//article[@id="nr"]')

    if _chapter_content:
        chapter_content = etree.tostring(_chapter_content[0], encoding='utf-8')
    else:
        chapter_content = ''

    return chapter_content


if __name__ == '__main__':
    check_update()
