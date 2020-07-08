# coding=UTF-8
import os
import requests
import re  #正则表达式模块
from urllib import parse  #用来拼接url
from bs4 import BeautifulSoup

website = "http://m.shuquge.com"
book_index = website + "/s/110282"
ebook_dir = "/tmp/ebook/"
ebook_file = ""


class HtmlParser(object):
    def parser(self):
        '''
        解析器主函数
        parm page_url:一个url
        parm html_cont:网页内容，格式为字符串
        return: urls, 数据；格式为 set, dict
        '''

        #  获取最新章节
        new_data = self._get_page_url()
        self._get_last_page(new_data)
        return new_data

    def get_concent(self, page_url):
        table_of_contents = book_index + ".html"
        res = requests.get(table_of_contents)
        if res.status_code != 200:
            print("抱歉，%s 页面飞了～" % table_of_contents)
        return res.content

    def get_soup(self, html_cont):
        return BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')

    def _get_page_url(self):
        '''
        提取想要的数据
        parm page_url: 当前页面url
        parm soup: beautifulsoup对象
        return: dict
        '''
        # 获取内容
        html_cont = self.get_concent(book_index)
        #建立bs对象，使用html.parser进行解析
        soup = self.get_soup(html_cont)
        #声明字典
        data = {}
        data['url'] = website + soup.find("li").find('a').get('href')
        data['title'] = soup.find('li').find('a').get_text()
        global ebook_file
        ebook_file = ebook_dir + data['title'].split().pop(0) + ".txt"
        return data

    def _get_last_page(self, page_info):

        content = ''
        for prefix in [None, "_2", "_3"]:
            if prefix:
                page_url = page_info["url"].replace(".html", prefix + ".html")
            else:
                page_url = page_info["url"]
            content_result = requests.get(page_url).content
            soup = BeautifulSoup(content_result, 'html.parser', from_encoding='urf-8')
            content += soup.find(id="nr").get_text()

        with open(ebook_file, "w") as f:
            f.write(content)


if __name__ == "__main__":
    new_data = HtmlParser().parser()
    print(new_data)
    print("请查看", ebook_file)
