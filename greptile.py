#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import shutil


def matches(rexpr, fname):
    with open(fname, 'r') as f:
        for line in f:
            if rexpr.search(line):
                return True
    return False


def matching_lines(rexpr, fname):
    with open(fname, 'r') as f:
        for n, line in enumerate(f):
            if rexpr.search(line):
                yield n, line


def compiled_re(rexpr):
    return hasattr(rexpr, 'match') and rexpr or re.compile(rexpr)


def grep_rl(pattern, root_dir, *file_types):
    r = compiled_re(pattern)
    for f in list_files(root_dir, *file_types):
        if matches(r, f):
            yield (f)


def sed(source, pattern, repl, dest=sys.stdout, only_first_occurrence=False):
    r = compiled_re(pattern)
    count = only_first_occurrence and 1 or 0
    new_l = None
    for l in source:
        new_l = count and new_l and l or r.sub(repl, l, count)
        dest.write(new_l)


def sed_i(files, pattern, repl, only_first_occurrence=False):
    r = compiled_re(pattern)
    count = only_first_occurrence and 1 or 0
    for f in files:
        with open(f, 'r') as source:
            tmp_f = f + '.pygrep.tmp'
            with open(tmp_f, 'w') as dest:
                new_l = None
                for l in source:
                    new_l = count and new_l and l or r.sub(repl, l, count)
                    dest.write(new_l)

        shutil.copymode(f, tmp_f)
        ori_f = f + '.pygrep.ori'
        os.rename(f, ori_f)
        os.rename(tmp_f, f)
        os.remove(ori_f)


def replace(pattern, repl, root_dir, *types):
    sed_i(grep_rl(pattern, root_dir, *types), pattern, repl)


def list_files(root_dir, *types):
    for root, _, files in os.walk(root_dir):
        for f in files:
            if not types or os.path.splitext(f)[-1] in types:
                yield os.path.join(root, f)


def main(pattern, filepath=None, recursive_dir=None, extensions=(), inplace=False,
         print_list=False, replace_first=None, replace_global=None):

    re_compile = re.compile(pattern)
    if recursive_dir:
        l = list_files(recursive_dir, *extensions)
        file_list = (f for f in l if matches(re_compile, f))
    else:
        file_list = filepath and (filepath,) or ()

    replace_pattern = replace_first or replace_global
    if replace_pattern:
        if inplace:
            sed_i(file_list, re_compile, replace_pattern, replace_first)
        else:
            if file_list:
                for f in file_list:
                    with open(f, 'r') as f:
                        sed(f, re_compile, replace_pattern, sys.stdout, replace_first)
            else:
                sed(sys.stdin, re_compile, replace_pattern, sys.stdout, replace_first)

    else:
        if not file_list:
            print "Need file argument"
        for f in file_list:
            if print_list:
                print f
            else:
                lines = matching_lines(re_compile, f)
                for n, l in lines:
                    if recursive_dir:
                        print f + ' ' + str(n) + ': ',
                    print l,


def argparsed_arguments():
    import argparse
    parser = argparse.ArgumentParser(
            description='file search and replace with regular expressions',
            version="1.0")

    parser.add_argument('-x', '--extensions', nargs='+', default=(),
                        help='restrict search to file extensions (ex: .py .txt .java .xml)')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recursively search in path')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list files matching pattern')
    parser.add_argument('-i', '--inplace', action='store_true',
                        help='update the file inplace (with -g or -f)')
    parser.add_argument('-g', '--replace-global',
                        help='replacement expression')
    parser.add_argument('-f', '--replace-first',
                        help='replacement expression')
    parser.add_argument('pattern',
                        help='regular expression')
    parser.add_argument('file', nargs="?",
                        help='file path (or directory if -r is used)')

    return parser.parse_args()

if __name__ == '__main__':

    parsed_args = argparsed_arguments()

    main(pattern=parsed_args.pattern,
         filepath=parsed_args.file,
         recursive_dir=parsed_args.recursive and (parsed_args.file or './'),
         extensions=parsed_args.extensions,
         inplace=parsed_args.inplace,
         print_list=parsed_args.list,
         replace_first=parsed_args.replace_first,
         replace_global=parsed_args.replace_global)
