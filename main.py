#!/usr/bin/python
# -*- coding: UTF-8 -*-

from service import reader, writer

# from flask import Flask

# app = Flask("exam helper")

if __name__ == '__main__':
    # app.run()
    reader = reader.ExcelReader()
    qs = reader.read("4.1-安全知识考试-一线人员-规章制度部分.xls")
    writer = writer.DocWriter("a.docx", qs)
    writer.write()
    writer.save()