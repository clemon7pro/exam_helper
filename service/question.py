#!/usr/bin/python
# -*- coding: UTF-8 -*-

from enum import IntEnum, unique
import json

@unique
class QuestionType(IntEnum):
    single_choice = 0
    multiple_choice = 1
    binary_choice = 2
    short_answer = 3
    
class Question(object):
    '''
        
    '''
    def __init__(self, question_type: QuestionType, stem: str, answer: list or str or bool, options: list = [], explain: str = "") -> None:
        self.__question_stem = stem
        self.__answer = answer
        self.__type = question_type
        self.__options = options
        self.__explain = explain
        
    @property
    def question_stem(self) -> str:
        return self.__question_stem
    
    @property
    def answer(self):
        return self.__answer
    
    @property
    def type(self) -> QuestionType:
        return self.__type
    
    @property
    def options(self):
        return self.__options
    
    @property
    def explain(self) -> str:
        return self.__explain
    
    def __str__(self) -> str:
        question = {
            "type": self.type,
            "question": self.question_stem,
            "answer": self.answer
        }
        match self.__type:
            case QuestionType.single_choice | QuestionType.multiple_choice:
                question["options"] = self.options
            case QuestionType.binary_choice:
                pass
            case QuestionType.short_answer:
                pass
        
        return json.dumps(question, ensure_ascii=False)
    