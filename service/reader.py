#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
from .question import *


class ExcelReader(object):
    def __init__(self) -> None:
        pass
    
    def read(self, file):
        
        model = {
            "question_stem": "试题内容",
            "answer": "参考答案",
            "question_type": "题型名称",
            "option_headers": ["A", "B", "C", "D", "E", "F"],
            "explain": "试题解析"
        }
        
        cols = [model["question_stem"], model["question_type"], model["answer"]] + [header for header in model["option_headers"]]
        raw_questions = pd.read_excel(file, usecols=cols)
        
        questions= []
        for _, raw_question in raw_questions.iterrows():
            
            match raw_question[model["question_type"]].strip():
                case "单选题" | "多选题":
                    options = []
                    for idx in model["option_headers"]:
                        if not pd.isna(raw_question[idx]):
                            options.append(str(raw_question[idx]).strip(idx+'-'))

                    answer = list(str(raw_question[model["answer"]]).strip().upper())
                    
                    questions.append(Question(
                        question_type=QuestionType.single_choice if raw_question[model["question_type"]] == "单选题" \
                                                                else QuestionType.multiple_choice,
                        stem=raw_question[model["question_stem"]].strip(),
                        answer=answer,
                        options=options
                        ))
                case "判断题":
                    questions.append(Question(
                        question_type=QuestionType.binary_choice,
                        stem=raw_question[model["question_stem"]].strip(),
                        answer=True if str(raw_question[model["answer"]]).upper() == "A" else False
                    ))
                case "简答题":
                    questions.append(Question(
                        question_type=QuestionType.short_answer,
                        stem=raw_question[model["question_stem"]].strip(),
                        answer=str(raw_question[model["answer"]]).strip()
                    ))
                case _:
                    pass
                
        return questions