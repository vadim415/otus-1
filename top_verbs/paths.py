# -*- coding: utf-8 -*-
import ast
import os
from pathlib import Path
import collections
from words import (
    filter_magic_methods,
    flat,
    get_verbs_from_function_name,
)


def get_filenames(path):
    """Возвращает список имён .py-файлов, находящихся внутри path."""
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith(".py"):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == 100:
                    break
    print(f"total {len(filenames)} files")
    return filenames


def get_trees(path, with_filenames=False, with_file_content=False):
    """Возвращает AST-деревья .py-файлов, находящийся внутри path."""
    filenames = get_filenames(path)
    trees = []
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as attempt_handler:
            main_file_content = attempt_handler.read()
            try:
                tree = ast.parse(main_file_content)
            except SyntaxError as e:
                print(e)
                tree = None
            if with_filenames:
                if with_file_content:
                    trees.append((filename, main_file_content, tree))
                else:
                    trees.append((filename, tree))
            elif tree:
                trees.append(tree)
    print("trees generated")
    return trees


def get_all_names(tree):
    """Возвращает все имена нод из дерева."""
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_top_verbs_in_path(path, top_size=10):
    """Возвращает самые популярные глаголы."""
    functions_names = get_functions_names_in_path(path)
    verbs = flat(
        [
            get_verbs_from_function_name(function_name)
            for function_name in functions_names
        ]
    )
    return collections.Counter(verbs).most_common(top_size)


def get_functions_names_in_path(path):
    """Возвращает названия функций."""
    trees = get_trees(path)
    functions_names = []
    for tree in trees:
        flat_names = [
            node.name.lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]
        functions_names.extend(flat_names)
    functions_names = filter_magic_methods(functions_names)
    print("functions extracted")
    return functions_names
