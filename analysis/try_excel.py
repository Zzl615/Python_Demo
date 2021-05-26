#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   try_excel.py
@Time    :   2021/05/26 22:11:22
@Author  :   Zzl
@Contact :   noaghzil@gmail.com
@Desc    :   None
'''

# here put the import lib

import pandas as pd

data = [['tom', 10], ['nick', 15], ['juli', 14]]

cls_name = ["Name", "Age"]

idx_name = ["rank1", "rank2"]

df = pd.DataFrame(data, columns=cls_name, index=idx_name)

file_path = "memeber.xlsx"

df.to_excel(file_path)
