# -*- encoding: utf-8 -*-
# 数据收集
# 功能： 定时、加cookies，拟人下载
# 搜索：标签、标题、地址
# 通用性的脚本
import os
import time
import urllib
import requests

# 账号cookie
cookies_str = ''

# 报文头
headers = {
    'Accept':
    '*/*',
    'Accept-Encoding':
    'gzip, deflate, br',
    'Accept-Language':
    'zh-CN,zh;q=0.9',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
    '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# 间隔时间：2s
sleep_time = 2

download_url = "http://xxx.com/fulltext/download/{download_id}"

detail_page = "http://xxx.com/literature/{page_id}"


def get_cookies_dict(cookies_str):
    """
    处理浏览器的cookies
    :param cookies_str:  str格式的cookies
    :return cookies_dict:  dict格式的cookies
    """
    cookies_dict = {}
    #按照字符：进行划分读取
    for line in cookies_str.split(';'):
        name, value = line.strip().split('=', 1)
        cookies_dict[name] = value
    return cookies_dict


cookies = get_cookies_dict(cookies_str)


def get_reponse_content(url, code='utf8', type="text"):
    """
    获取请求相应
    :param url:  请求地址
    :param code:  编码格式
    :param type:  resp处理方式
    :return content: 请求内容
    """
    try:
        resp = requests.get(url, headers=headers, cookies=cookies, stream=True)
        resp.raise_for_status()
        resp.encoding = code
        content = getattr(resp, type, "text")
        return content
    except Exception as e:
        print("%s 请求失败 error: %s" % (url, e))
        raise


def get_location_url(url):
    """
    获取真实URL地址
    :param url:  请求地址
    :param headers:  请求报头
    :param cookies:  携带cookies
    :return r.headers['Location']: 真实URL地址
    """
    try:
        resp = requests.head(url, headers=headers, cookies=cookies, stream=True)
        #print(resp.headers)
        resp.raise_for_status()
        location_url = None
        if resp.status_code == 301:
            location_url = resp.headers['Location']
        return location_url
    except Exception as e:
        print("%s 请求失败 error: %s" % (url, e))
        raise


def get_filename(url):
    """
    获取真实URL地址
    :param url:  请求地址
    :return filename: 文件名
    """
    filename = urllib.parse.unquote(os.path.basename(url))
    return filename


def getPDFContent(url, headers, cookies, code='utf8'):
    """
    PDF信息预处理
    """
    pass


def pointLiterature(filename):
    """
    记录需要积分的文献
    """
    src_dir = '/Users/kfz/Project/Private/Python_Demo/Olds'
    point_file = src_dir + '/point.txt'
    with open(point_file, "a") as f:
        f.write(filename)

    print("Point:", filename)


if __name__ == "__main__":
    for num in range(1, 11):
        analysis_url = download_url.format(download_id=num)
        location_url = get_location_url(analysis_url)
        if location_url:
            # 文件夹
            filename = get_filename(location_url)
            fulltext = get_reponse_content(analysis_url, type="content")
            # TODO：大文件处理
            with open(filename, 'wb') as f:
                f.write(fulltext)
        else:
            pointLiterature(analysis_url)
        time.sleep(sleep_time)
