# -*- coding: utf-8 -*-
from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word=None):
    """
    Возвращает True, если слово глагол.
    """
    if word:
        pos_info = pos_tag([word])
        return pos_info[0][1] == "VB"
    return False


def split_snake_case_name_to_words(name):
    """
    Разделяет строку на слова по разделителю _.
    """
    return [n for n in name.split("_") if n]


def filter_magic_methods(list_of_methods):
    """
    Возвращает всё, кроме магических имён.
    """
    return [
        f for f in list_of_methods
        if not (f.startswith("__") and f.endswith("__"))
    ]


def get_verbs_from_function_name(function_name):
    """
    Возвращает все глаголы из имён функций.
    """
    return [word for word in function_name.split("_") if is_verb(word)]
