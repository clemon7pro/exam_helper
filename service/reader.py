#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import Any
from bs4 import BeautifulSoup
import pandas as pd
from .question import Question, QuestionType


def _def_opts_handler(raw_opts: Any) -> list:
    opts = []
    for opt in raw_opts:
        opts.append(str(opt))
    return opts


def _def_ans_handler(type: QuestionType, ans: Any) -> list | str | bool:
    return list(ans)


class ExcelReader(object):
    def __init__(
        self, model: dict, skiprows=0, opts_handler=None, ans_handler=None
    ) -> None:
        self._model = model
        self._skiprows = skiprows
        self._opts_handler = _def_opts_handler if opts_handler is None else opts_handler
        self._ans_handler = (
            _def_ans_handler if ans_handler is None else ans_handler
        )

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
                    options = self._opts_handler(raw_options)

                    question_type = (
                        QuestionType.single_choice
                        if raw_question[self._model["question_type"]] == "单选"
                        else QuestionType.multiple_choice
                    )
                    answer = self._ans_handler(
                        question_type,
                        str(raw_question[self._model["answer"]]).strip().upper(),
                    )

                    questions.append(
                        Question(
                            question_type=question_type,
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
            for raw_question in soup.select(".TMBorder .problem"):
                index = raw_question.get("index")
                # 题干
                stem = raw_question.select_one(".TMTitle").text.strip()

                # 选项
                options = []
                for op in raw_question.select_one(".TMContent").select("tr"):
                    # o = tds[0].select_one("input").get("value")
                    options.append(
                        op.select("td")[1].select_one(".TMOption").text.strip()
                    )

                # 答案
                ans = raw_question.select_one("#topicKey_{}".format(index)).get("value")
                type = raw_question.select_one("#baseType_{}".format(index)).get(
                    "value"
                )

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

        return questions
