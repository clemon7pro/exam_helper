#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pstats
from bs4 import BeautifulSoup
import pandas as pd
from .question import Question, QuestionType


def defOptsHandler(rawOpts: any) -> list:
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
        cols = [
            self._model["question_stem"],
            self._model["question_type"],
            self._model["explain"],
            self._model["answer"],
        ] + [header for header in self._model["option_headers"]]
        raw_questions = pd.read_excel(file, usecols=cols, skiprows=self._skiprows)

        questions = []
        for _, raw_question in raw_questions.iterrows():
            explain = ""
            if not pd.isna(raw_question[self._model["explain"]]):
                explain = str(raw_question[self._model["explain"]])

            stem = (
                raw_question[self._model["question_stem"]]
                .strip()
                .replace("\n", "")
                .replace("\r", "")
            )

            match raw_question[self._model["question_type"]].strip():
                case "单选题" | "多选题" | "单选" | "多选":
                    raw_options = []
                    for idx in self._model["option_headers"]:
                        if not pd.isna(raw_question[idx]):
                            raw_options.append(raw_question[idx])
                    options = self._optsHandler(raw_options)

                    answer = list(
                        str(raw_question[self._model["answer"]]).strip().upper()
                    )

                    questions.append(
                        Question(
                            question_type=QuestionType.single_choice
                            if raw_question[self._model["question_type"]] == "单选题"
                            else QuestionType.multiple_choice,
                            stem=stem,
                            answer=answer,
                            options=options,
                            explain=explain,
                        )
                    )
                case "判断题":
                    raw_ans = str(raw_question[self._model["answer"]]).upper()
                    questions.append(
                        Question(
                            question_type=QuestionType.binary_choice,
                            stem=stem,
                            answer=True
                            if raw_ans == "A" or raw_ans == "对" or raw_ans == "正确"
                            else False,
                            explain=explain,
                        )
                    )
                case "简答题":
                    questions.append(
                        Question(
                            question_type=QuestionType.short_answer,
                            stem=stem,
                            answer=str(raw_question[self._model["answer"]]).strip(),
                            explain=explain,
                        )
                    )
                case _:
                    pass

        return questions


class DocxReader(object):
    def __init__(self) -> None:
        pass


class GWXTHtmlReader(object):
    def __init__(self) -> None:
        pass

    def read(self, file):
        questions = []
        with open(file) as f:
            soup = BeautifulSoup(f, "html.parser")
            for problem in soup.select(".TMBorder .problem"):
                index = problem.get("index")
                # 题干
                stem = problem.select_one(".TMTitle").text.strip()

                # 选项
                options = []
                for op in problem.select_one(".TMContent").select("tr"):
                    tds = op.select("td")
                    # o = tds[0].select_one("input").get("value")
                    options.append(tds[1].select_one(".TMOption").text.strip())
                    
                flg = []
                for i, opt in enumerate(options):
                    if opt[0] == "ABCDEFGHIJK"[i]:
                        flg.append(True)
                    else:
                        break
                if len(flg) == len(options):
                    o = []
                    for i, opt in enumerate(options):
                        o.append(opt[1:])
                    options = o

                # 答案
                ans = problem.select_one("#topicKey_{}".format(index)).get("value")
                type = problem.select_one("#baseType_{}".format(index)).get("value")

                match str(type):
                    case "1":
                        questions.append(
                            Question(
                                question_type=QuestionType.single_choice,
                                stem=stem,
                                answer=ans,
                                options=options,
                            )
                        )
                    case "2":
                        questions.append(
                            Question(
                                question_type=QuestionType.multiple_choice,
                                stem=stem,
                                answer=ans,
                                options=options,
                            )
                        )
                    case "4":
                        questions.append(
                            Question(
                                question_type=QuestionType.binary_choice,
                                stem=stem,
                                answer=True if str(ans).upper() == "A" else False,
                            )
                        )
                # if len(options) == 2 and "对" in options and "错" in options:

                # if len(ans) > 1:

                #     continue

                # if len(ans) == 1:

        return questions
