import os
from shutil import copy2
from googletrans import Translator

src_dir = '~/Olds'               #源文件目录地址
des_dir = '~/News'               #新文件目录地址
num = 0

if not os.path.exists(des_dir):		#如果没有目标文件夹,新建一个目标文件夹进行存储
    os.makedirs(des_dir)

if os.path.exists(src_dir):
    dirs = os.listdir(src_dir)          #获取源文件的目录地址
    translator = Translator(service_urls=['translate.google.cn'])    
    for dirc in dirs:                     #对于目录下的每一个文件
        if "pdf" not in dirc:
            continue   
        paper_title = dirc.replace('.pdf','').replace('+',' ')
        paper_title = translator.translate(paper_title, dest='zh-CN').text
        import re
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        if zh_pattern.search(paper_title):
            print(paper_title)
            if paper_title.find('/') != -1:       #对于'/'无法写入文件名的情况,将其用'_'代替
                new_paper_title = paper_title.replace('/','_')
                paper_title = new_paper_title
                copy2(os.path.join(src_dir, dirc), os.path.join(des_dir, paper_title) + '.pdf')
            else:
                copy2(os.path.join(src_dir, dirc), os.path.join(des_dir, paper_title) + '.pdf')
        
else:
    print("该路径下不存在所查找的目录!")