#!/usr/bin/python
# -*- coding: UTF-8 -*-
from service import reader, writer
import re

def delmOptsHandler(rawOpts : any) -> list:
    opts = []
    for opt in re.split('\\$;\\$', str(rawOpts[0])):
        opts.append(re.sub('[A-F]{1}-', '', opt))
    return opts

if __name__ == '__main__':
    base_path = '/Users/clemon/Desktop/'
    name = '变电运维（监控）班'

    x = reader.ExcelReader({
            "question_stem": "试题正文",
            "answer": "试题答案",
            "question_type": "题型",
            "option_headers": ["试题选项"],
            "explain": "依据 出处"
        }, skiprows=1, optsHandler=delmOptsHandler)
    q = x.read(base_path + name + '.xls')
    
    # 小包搜题
    w = writer.XiaobaosoutiWriter(base_path + '小包-' + name + '.txt', q)
    w.write()
    w.save()
    
    # word文档
    # w = writer.DocWriter(base_path + '.docx', q)
    # w.write()
    # w.save()
    
    # 考试宝
    # w = writer.KaoshibaoWriter(base_path + 'xb-安规-主业产业人员-变电安规.xlsx', q)
    # w.write()
    # w.save()