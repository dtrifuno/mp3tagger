import argparse
import os
import re
from typing import List

from mutagen.id3 import APIC, ID3
from mutagen.mp3 import EasyMP3

from .process import process_file
from .tags import formula_to_regex, TAG_TO_GROUP


DEFAULT_FORMULA = r'%ARTIST/%YEAR - %ALBUM/%TRACK_NUM - %TRACK_TITLE.mp3'


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Automatically tag MP3 files by inferring tags from directory structure.')
    parser.add_argument('PATH', help="directory path")
    parser.add_argument('-f', metavar='FORMULA', default=DEFAULT_FORMULA,
                        help=f"directory structure formula (default: \"{DEFAULT_FORMULA.replace('%', '%%')}\")")
    parser.add_argument('-d', action='store_true',
                        help="delete all tags not present in formula")
    parser.add_argument('-c', action='store_true',
                        help="attach \"cover.jpg\" as ID3 cover art whenever present")
    return parser


def create_file_list(path: str) -> List[str]:
    result = []
    for dir_, _, files in os.walk(path):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, path)
            rel_file = os.path.join(rel_dir, file_name)
            result.append(rel_file)
    return result


def main():
    parser = create_parser()
    args = parser.parse_args()
    path = args.PATH
    formula = args.f
    delete = args.d
    cover = args.c

    file_list = create_file_list(path)
    regex = formula_to_regex(formula)
    for file_path in file_list:
        process_file(path, file_path, regex, delete=delete, cover=cover)
