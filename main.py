#!/usr/bin/python
# -*- coding: UTF-8 -*-
from service import reader, writer
import re
import os

def delmOptsHandler(rawOpts : any) -> list:
    opts = []
    for opt in re.split('\\|', str(rawOpts[0])):
        opts.append(re.sub('[A-F]{1}-', '', opt))
    return opts

def e():
    base_path = '/Users/clemon/Desktop/上海公司整合版本/安全知识考试-四类人员-规章制度部分（整合后）/'
    
    for f in os.listdir(base_path):
        if f == ".DS_Store":
            continue
        print("processing {} ....".format(f))

        x = reader.ExcelReader({
                "question_stem": "题干",
                "answer": "答案",
                "question_type": "题型",
                "option_headers": ["选项"],
                "explain": "题目依据"
            }, optsHandler=delmOptsHandler)
        q = x.read(base_path + f)
        
        # 小包搜题
        # w = writer.XiaobaosoutiWriter('/Users/clemon/Desktop/2024版小包题库/' + os.path.splitext(f)[0] + '.txt', q)
        # w.write()
        # w.save()
    
        # word文档
        # w = writer.DocWriter(base_path + '.docx', q)
        # w.write()
        # w.save()
    
        # 考试宝
        w = writer.KaoshibaoWriter('/Users/clemon/Desktop/上海公司整合版本/规章制度部分-考试宝/' + os.path.splitext(f)[0] + '.xlsx', q)
        w.write()
        w.save()

if __name__ == '__main__':
    name = "（国网）技能等级评价电力调度员（主网）专业知识考试练习-中级工"
    q = reader.GWXTHtmlReader().read("/Users/clemon/Desktop/" + name + ".html")
    w = writer.KaoshibaoWriter('/Users/clemon/Desktop/' + name + '.xlsx', q)
    w.write()
    w.save()