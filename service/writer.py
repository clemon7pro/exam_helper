#!/usr/bin/python
# -*- coding: UTF-8 -*-
from docx import Document
import math

from .question import *

class DocWriter(object):
    
    def __init__(self, file, questions: list) -> None:
        self.__doc = Document()
        self.__file = file
        self.__questions = questions
        
    def __write_single(self, id: int, question: Question):
        self.__doc.add_paragraph("第" + str(id) + "题. " + question.question_stem)
        answer = "#err"
        
        match question.type:
            case QuestionType.single_choice | QuestionType.multiple_choice:
                col_len = 2
                row_len = int(math.ceil(len(question.options) / col_len))
                table = self.__doc.add_table(rows=row_len, cols=col_len)
                
                for i, v in enumerate(question.options):
                    table.cell(int(divmod(i, col_len)[0]), int(divmod(i, col_len)[1])).text = chr(65+i)+". " + v
                    
                answer = "".join(question.answer)
            case QuestionType.binary_choice:
                answer = "对" if question.answer else "错"
            case QuestionType.short_answer:
                answer = question.answer
                
        self.__doc.add_paragraph("答案: " + answer)
    
    def write(self):
        single_choice_questions = list(filter(lambda item: item.type == QuestionType.single_choice, self.__questions))
        multiple_choice_questions = list(filter(lambda item: item.type == QuestionType.multiple_choice, self.__questions))
        binary_choice_questions = list(filter(lambda item: item.type == QuestionType.binary_choice, self.__questions))
        short_answer_questions = list(filter(lambda item: item.type == QuestionType.short_answer, self.__questions))
        
        id = 1
        if len(single_choice_questions):
            self.__doc.add_paragraph("单选题: ")
            for question in single_choice_questions:
                self.__write_single(id, question)
                self.__doc.add_paragraph()
                id += 1
                
        if len(multiple_choice_questions):
            self.__doc.add_paragraph("多选题: ")
            for question in multiple_choice_questions:
                self.__write_single(id, question)
                self.__doc.add_paragraph()
                id += 1
                
        if len(binary_choice_questions):
            self.__doc.add_paragraph("判断题: ")
            for question in binary_choice_questions:
                self.__write_single(id, question)
                self.__doc.add_paragraph()
                id += 1
        
        if len(short_answer_questions):
            self.__doc.add_paragraph("简答题: ")
            for question in short_answer_questions:
                self.__write_single(id, question)
                self.__doc.add_paragraph()
                id += 1
        
    def save(self):
        self.__doc.save(self.__file)

class XiaoBaoWriter(object):
    pass

class KaoShiBaoWriter(object):
    pass