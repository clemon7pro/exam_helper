#!/usr/bin/python
# -*- coding: UTF-8 -*-
from service import reader, writer
import re
import os


def delmOptsHandler(rawOpts: any) -> list:
    opts = []
    rawOpts = str(rawOpts[0]).replace("\n", "").replace("\r", "").strip()
    
    for opt in re.split("\\$;\\$", rawOpts):
        opts.append(re.sub("[A-F]{1}-", "", opt.strip()))
    return opts


def process_one(in_file, out_file):
    x = reader.ExcelReader(
        {
            "question_stem": "试题",
            "answer": "试题答案",
            "question_type": "题型",
            "option_headers": ["试题选项"],
            "explain": "题目依据",
        },
        optsHandler=delmOptsHandler,
    )
    q = x.read(in_file)

    # 小包搜题
    w = writer.XiaobaosoutiWriter(out_file, q)
    w.write()
    w.save()

    # word文档
    # w = writer.DocWriter(base_path + '.docx', q)
    # w.write()
    # w.save()

    # 考试宝
    # w = writer.KaoshibaoWriter(
    #     out_file,
    #     q,
    # )
    # w.write()
    # w.save()


def process_all():
    base_path = "/Users/clemon/Desktop/上海公司整合版本/安全知识考试-四类人员-规章制度部分（整合后）/"

    for f in os.listdir(base_path):
        if f == ".DS_Store":
            continue
        print("processing {} ....".format(f))
        process_one(f, f)


if __name__ == "__main__":
    process_one(
        "/Users/clemon/Downloads/集控系统维护及应用专题培训班-题库.xlsx",
        "/Users/clemon/Downloads/out集控系统维护及应用专题培训班-题库.xlsx",
    )
