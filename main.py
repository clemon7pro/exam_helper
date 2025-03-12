#!/usr/bin/python
# -*- coding: UTF-8 -*-
from service import reader, writer
import re
import os


def delm_opts_handler(rawOpts: any) -> list:
    opts = []
    rawOpts = str(rawOpts[0]).strip().split("$|$")

    # re.split("\\|?[BCDEF]{1}[、-]{1}", rawOpts)
    for opt in rawOpts:
        opts.append(re.sub("[A-F]{1}[、-]{1}", "", opt.strip()))

    return opts

def ans_handler(type, ans):
    
    return str(ans).replace("、", "").replace("1", "A").replace("2", "B").replace("3", "C").replace("4", "D").replace("5", "E")

def process_one(in_file, out_file):
    x = reader.ExcelReader(
        {
            "question_stem": "题目内容",
            "answer": "参考答案",
            "question_type": "题目类型",
            # "option_headers": ["A", "B", "C", "D", "E"],
            "option_headers": [
                "选项1",
                "选项2",
            ],
            "explain": "考核知识点",
        },
        # opts_handler=delm_opts_handler,
        ans_handler=ans_handler,
    )
    q = x.read(in_file)
    # for i, item in enumerate(q):
    #     for op in item.options:
    #         if "|" in op:
    #             print("==========="+str(i+2)+"===============")
    #             print("{}: {}".format(item.question_stem,item.options))
    #             print("==========================")
    #             break

    # 小包搜题
    # w = writer.XiaobaosoutiWriter(out_file, q)
    # w.write()
    # w.save()

    # word文档
    # w = writer.DocWriter(base_path + '.docx', q)
    # w.write()
    # w.save()

    # 考试宝
    w = writer.KaoshibaoWriter(
        out_file,
        q,
    )
    w.write()
    w.save()


def process_all():
    base_path = "/Users/clemon/Desktop/换流站/"

    for f in os.listdir(base_path):
        if f == ".DS_Store":
            continue
        print("processing {} ....".format(f))
        p = "{}/{}".format(base_path, f)
        process_one(p, p)


if __name__ == "__main__":
    # process_all()
    process_one(
        "/Users/clemon/Desktop/2.判断题-已修订.xls",
        "/Users/clemon/Desktop/1.考试宝-判断题-已修订.xlsx",
    )
