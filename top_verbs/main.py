# -*- coding: utf-8 -*-
import os
import collections
from paths import get_top_verbs_in_path
from pathlib import Path

def main():
    words = list()
    projects = [
        "django",
        "flask",
        "pyramid",
        "reddit",
        "requests",
        "sqlalchemy",
    ]
    for project in projects:
        path = os.path.join(".", project)
        if Path(path).is_dir:
            words += get_top_verbs_in_path(path)

    top_size = 200
    print(f"total {len(words)} words, {len(set(words))} unique")
    for word, occurence in collections.Counter(words).most_common(top_size):
        print(word, occurence)


if __name__ == "__main__":
    main()
