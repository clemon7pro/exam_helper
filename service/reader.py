#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
from .question import Question, QuestionType

def defOptsHandler(rawOpts : any) -> list:
    opts = []
    for opt in rawOpts:
        opts.append(str(opt))
    return opts

class ExcelReader(object):
    def __init__(self, model, skiprows=0, optsHandler=None) -> None:
        self._model = model
        self._skiprows = skiprows
        if optsHandler is None:
            self._optsHandler = defOptsHandler
        else:
            self._optsHandler = optsHandler
    
    def read(self, file):
        cols = [self._model["question_stem"], self._model["question_type"], self._model["explain"], self._model["answer"]] + [header for header in self._model["option_headers"]]
        raw_questions = pd.read_excel(file, usecols=cols, skiprows=self._skiprows)
        
        questions= []
        for _, raw_question in raw_questions.iterrows():
            explain=""
            if not pd.isna(raw_question[self._model["explain"]]):
                explain=str(raw_question[self._model["explain"]])
                
            match raw_question[self._model["question_type"]].strip():
                case "单选题" | "多选题" | "单选" | "多选":
                    raw_options = []
                    for idx in self._model["option_headers"]:
                        if not pd.isna(raw_question[idx]):
                            raw_options.append(raw_question[idx])
                    options = self._optsHandler(raw_options)
                    
                    answer = list(str(raw_question[self._model["answer"]]).strip().upper())
                    
                    questions.append(Question(
                        question_type=QuestionType.single_choice if raw_question[self._model["question_type"]] == "单选题" \
                                                                else QuestionType.multiple_choice,
                        stem=raw_question[self._model["question_stem"]].strip(),
                        answer=answer,
                        options=options,
                        explain=explain
                        ))
                case "判断题":
                    questions.append(Question(
                        question_type=QuestionType.binary_choice,
                        stem=raw_question[self._model["question_stem"]].strip(),
                        answer=True if str(raw_question[self._model["answer"]]).upper() == "A" else False,
                        explain=explain
                    ))
                case "简答题":
                    questions.append(Question(
                        question_type=QuestionType.short_answer,
                        stem=raw_question[self._model["question_stem"]].strip(),
                        answer=str(raw_question[self._model["answer"]]).strip(),
                        explain=explain
                    ))
                case _:
                    pass
                
        return questions
    
    
class DocxReader(object):
    def __init__(self) -> None:
        pass