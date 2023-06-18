#!/usr/bin/python
# -*- coding: UTF-8 -*-
from service import reader, writer

if __name__ == '__main__':
    reader = reader.ExcelReader()
    q = reader.read("4.1-安全知识考试-一线人员-规章制度部分.xls")
    # 小包搜题
    w = writer.XiaobaosoutiWriter("aaa.txt", q)
    w.write()
    w.save()
    # word文档
    w = writer.DocWriter("aaa.docx", q)
    w.write()
    w.save()
    # 考试宝
    w = writer.KaoshibaoWriter("aaa.xlsx", q)
    w.write()
    w.save()