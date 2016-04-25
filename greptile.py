#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import os
import sys
import shutil


def _list_files(root_dir, *dot_extensions):
    for root, _, files in os.walk(root_dir):
        for f in files:
            f_ext = os.path.splitext(f)[-1]
            if not dot_extensions or f_ext in dot_extensions:
                yield os.path.join(root, f)


def _matches(expr, filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if expr.search(line):
                return True
    return False


def _matching_lines(expr, filepath):
    with open(filepath, 'r') as f:
        for n, line in enumerate(f):
            if expr.search(line):
                yield n, line


def _compiled_re(expr):
    return hasattr(expr, 'match') and expr or re.compile(expr)


def grep_rl(expr, root_dir, *dot_extensions):
    """
    Recursively walk from root_dir, selecting files by the provided extensions,
    and return those files having a line matching expr.

    Similar to:

    grep -rl expr [root_dir]

    :param expr: str or pattern
    :param root_dir:
    :param dot_extensions: file extensions or all files
    """
    r = _compiled_re(expr)
    for f in _list_files(root_dir, *dot_extensions):
        if _matches(r, f):
            yield (f)


def sed(source, expr, replace_exp, destination=sys.stdout, only_first_occurrence=False):
    """
    Search/replace matching expr from source to destination.

    Similar to:

    sed "s/expr/replace_expr/g" source > dest

    :type source: enumerate
    :type destination: file
    :param source: is a text line generator
    :type expr: str or pattern
    :type replace_exp: str
    :param destination: output stream
    :param only_first_occurrence: replace only first occurrence per line
    """
    r = _compiled_re(expr)
    count = only_first_occurrence and 1 or 0
    for l in source:
        new_l = r.sub(replace_exp, l, count)
        destination.write(new_l)


def sed_i(files, expr, replace_exp, only_first_occurrence=False):
    """
    Massively search/replace matching lines in files.

    Similar to:

    sed -i "s/expr/replace_expr/g" files...

    :type files: enumerate or list
    :param files: file names generator
    :type expr: str or pattern
    :type replace_exp: str
    :param only_first_occurrence: replace only first occurrence per line
    """
    r = _compiled_re(expr)
    for f in files:
        with open(f, 'r') as source:
            tmp_f = f + '.pygrep.tmp'
            with open(tmp_f, 'w') as dest:
                sed(source, r, replace_exp, dest, only_first_occurrence)

        shutil.copymode(f, tmp_f)
        ori_f = f + '.pygrep.ori'
        os.rename(f, ori_f)
        os.rename(tmp_f, f)
        os.remove(ori_f)


def replace(expr, replace_exp, root_dir, *dot_extensions):
    """
    THIS FUNCTION EFFECTIVELY MODIFY YOUR FILES CONTENTS !!!

    Recursively walk from root_dir, selecting files by the provided extensions,
    and massively search/replace matching lines.

    Similar to:

    grep -rl expr root_dir | sed -i "s/expr/replace_expr/g"

    :type expr: str
    :type replace_exp: str
    :type root_dir: str
    :param expr:
    :param replace_exp:
    :param root_dir:
    :param dot_extensions: file extensions or all files
    """
    sed_i(grep_rl(expr, root_dir, *dot_extensions), expr, replace_exp)


# ### COMMAND LINE INTERFACE ####


def _argv_parsed_arguments():
    import argparse

    parser = argparse.ArgumentParser(
            description='file search and replace with regular expressions')

    parser.add_argument('-x', '--extensions', nargs='+', default=(),
                        help='restrict search to file extensions (ex: .py .txt .java .xml)')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recursively search in path')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list files matching pattern')
    parser.add_argument('-i', '--inplace', action='store_true',
                        help='update the file inplace (with -g or -f)')
    parser.add_argument('-g', '--replace-global', metavar='REPLACE_EXPR',
                        help='global replacement expression')
    parser.add_argument('-f', '--replace-first', metavar='REPLACE_EXPR',
                        help='first occurrence replacement expression')
    parser.add_argument('expression',
                        help='regular expression')
    parser.add_argument('file', nargs="?",
                        help='file path (or directory if -r is used)')

    return parser.parse_args()


def _process_args(expression, filepath=None, recursive_dir=None, extensions=(), inplace=False,
                  print_list=False, replace_first=None, replace_global=None):

    compiled_expr = re.compile(expression)
    if recursive_dir:
        l = _list_files(recursive_dir, *extensions)
        file_list = (f for f in l if _matches(compiled_expr, f))
    else:
        file_list = filepath and (filepath,) or ()

    replace_expr = replace_first or replace_global
    if replace_expr:
        if inplace:
            sed_i(file_list, compiled_expr, replace_expr, replace_first)
        else:
            if file_list:
                for f in file_list:
                    with open(f, 'r') as f:
                        sed(f, compiled_expr, replace_expr, sys.stdout, replace_first)
            else:
                sed(sys.stdin, compiled_expr, replace_expr, sys.stdout, replace_first)

    else:
        if not file_list:
            print("Need file argument")
        for f in file_list:
            if print_list:
                print(f)
            else:
                lines = _matching_lines(compiled_expr, f)
                for n, l in lines:
                    if recursive_dir:
                        print(f + ' ' + str(n) + ': ', end=' ')
                    print(l, end=' ')


def main():
    parsed_args = _argv_parsed_arguments()

    _process_args(expression=parsed_args.expression,
                  filepath=parsed_args.file,
                  recursive_dir=parsed_args.recursive and (parsed_args.file or './'),
                  extensions=parsed_args.extensions,
                  inplace=parsed_args.inplace,
                  print_list=parsed_args.list,
                  replace_first=parsed_args.replace_first,
                  replace_global=parsed_args.replace_global)


if __name__ == '__main__':
    main()
