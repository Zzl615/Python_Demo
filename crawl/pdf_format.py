import os
import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer
import PyPDF2 
from shutil import copy2

src_dir = '~/Olds'               #源文件目录地址
des_dir = '~/News'               #新文件目录地址
num = 0

if not os.path.exists(des_dir):		#如果没有目标文件夹,新建一个目标文件夹进行存储
    os.makedirs(des_dir)

if os.path.exists(src_dir):
    dirs = os.listdir(src_dir)          #获取源文件的目录地址
    print(dirs)
    for dirc in dirs:                     #对于目录下的每一个文件
        if "pdf" not in dirc:
            continue               
        fd = open(os.path.join(src_dir, dirc), 'rb')
        doc = PDFDocument(fd)      #打开并建立一个PDF文件对象
        viewer = SimplePDFViewer(fd)
        reader = PyPDF2.PdfFileReader(fd)
        print(reader.documentInfo)
        #print(reader.getPage(0).extractText())
        #paper_title = pdf_reader.getDocumentInfo()                         #获取PDF标题
        viewer.render()
        #print(doc.root)
        #print(viewer.canvas.text_content)
        #print("num : %s" % num , doc)                                    #终端显示处理到第几个文件
        # num += 1
        # paper_title = str(paper_title)                                           #标题字符化
        
        # if paper_title.find('/') != -1:       #对于'/'无法写入文件名的情况,将其用'_'代替
        #     new_paper_title = paper_title.replace('/','_')
        #     paper_title = new_paper_title
        #     copy2(os.path.join(src_dir, dirc), os.path.join(des_dir, paper_title) + '.pdf')
        # else:
        #     copy2(os.path.join(src_dir, dirc), os.path.join(des_dir, paper_title) + '.pdf')
        
else:
    print("该路径下不存在所查找的目录!")