#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Date          : 2020/09/21 10:58:08
@Author        : 张宗梁｜zhangzongliang@zuoshouyisheng.com
@Description   : "流式下载: 对大压缩文件下载（>1GiB）"
'''
from flask import Flask
from flask import Response
from flask import stream_with_context
app = Flask(__name__)

import os 
import requests
import zipstream

chunk_size = 10

@app.route("/download/<file_path>", methods=["GET"])
def download(file_path):
    """
      流式下载
    """
    def generate():
        """
          生成器，迭代读取文件，进行传输
        """
        global chunk_size
        if not os.path.exists(file_path):
            raise "File not found."
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                print(chunk)
                yield chunk

    # 运行 Flask app，可以正确下载文件，但是下载只有实时速度，没有文件总大小，导致无法知道下载进度，也没有文件类型，这些我们都可以通过增加 header 字段实现：
    # return Response(generate(), content_type="application/octet-stream")

    response = Response(generate(), mimetype='application/gzip')
    response.headers['Content-Disposition'] = 'attachment; filename={}.tar.gz'.format("download_file")
    response.headers['content-length'] = os.stat(str(file_path)).st_size
    return response

@app.route("/download1/<file_path>", methods=["GET"])
def transfer_download(file_path):
    """
     转发流式下载：
        1. 集群中的任一节点，均可下载集群中所有节点的指定文件 (转发列表，映射资源位置)
        2. 实现转发并实时下载，避免访问节点占用太多内存（stream_with_context）
    """
    url_file_map = {"zipfile.zip":"http://1.1.1.1/"} 
    url_prefix = url_file_map[file_path]
    remote_url = url_prefix + file_path
    req = requests.get(remote_url, stream = True)
    return Response(stream_with_context(req.iter_content()), 
                    content_type = req.headers['content-type'])

@app.route("/download2/<file_path>", methods=["GET"])
def cluster_download(file_path):
    """
     多节点并实时压缩下载: 

    """
    def generate_file(content):
        yield content

    def generate(req):
        """
          生成器，迭代读取文件，进行传输
        """
        global chunk_size
        z = zipstream.ZipFile(mode="w", compression=zipstream.ZIP_DEFLATED)
        for req in reqs:
            host = req.raw._fp.fp._sock.getpeername()[0]
            z.write_iter("%s.tar.gz" % host, req.iter_content(chunk_size=chunk_size))
        z.write_iter("running_status", generate_file("hello world!"))
        for chunk in z:
            yield chunk

    def get_file_size(reqs):
        size = 0
        for req in reqs:
            size += int(req.headers.get("content-length"))
        return size

    remote_hosts = ["1.1.1.1", "2.2.2.2"]
    reqs = []
    for host in remote_hosts:
        req = requests.get("http://%s/%s" % (host, file_path), timeout=5, stream=True)
        if req.status_code == 200:
            reqs.append(req)
    response = Response(generate(reqs))
    response.headers['mimetype'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename=cluster_logs.zip'
    response.headers['content-length'] = get_file_size(reqs)
    return Response(response, content_type = response.headers['content-type'])

@app.route('/index')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    # 启动方式一：
    app.run(host="0.0.0.0", port=5000, debug=True)
    # 启动方式二：
    # export FLASK_APP=stream.py
    # flask run