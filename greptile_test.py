#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import shutil

try:
    import StringIO as io
except ImportError:
    import io

import unittest
import greptile
import re
import difflib


class MyTestCase(unittest.TestCase):

    def test_matching_file(self):
        self.assertEqual(['./test/LICENSE.txt'], [l for l in greptile.grep_rl('GNU', './test', '.txt')])
        self.assertEqual([], [l for l in greptile.grep_rl('BLABLA', './test', '.txt')])

    def test_matching_lines(self):
        self.assertEqual([
            (39, 'Application, but excluding the System Libraries of the Combined Work.\n'),
            (127, '  5. Combined Libraries.\n')
        ],
                [l for l in greptile._matching_lines(re.compile('Libraries'), './test/LICENSE.txt')])
        self.assertEqual([],
                [l for l in greptile._matching_lines(re.compile('BLABLA'), './test/LICENSE.txt')])

    def test_matching_sed(self):
        sio = io.StringIO()
        with open('./test/LICENSE.txt', 'r') as f:
            greptile.sed(f, 'Material', 'Spam', sio)

        with open('./test/LICENSE.txt', 'r') as f:
            self.assertEqual([
                '-  3. Object Code Incorporating Material from Library Header Files.\n',
                '+  3. Object Code Incorporating Spam from Library Header Files.\n'],
                 [l for l in difflib.unified_diff(f.readlines(), sio.getvalue().splitlines(1))][6:8])

    def test_replace(self):
        license_copy = './test/LICENSE_COPY.tmp'
        shutil.copy('./test/LICENSE.txt', license_copy)
        try:
            greptile.replace('Material', 'Spam', './test', '.tmp')
            with open('./test/LICENSE.txt', 'r') as f:
                with open(license_copy, 'r') as f2:
                    self.assertEqual([
                        '-  3. Object Code Incorporating Material from Library Header Files.\n',
                        '+  3. Object Code Incorporating Spam from Library Header Files.\n'],
                            [l for l in difflib.unified_diff(f.readlines(), f2.readlines())][6:8])
        finally:
            os.remove(license_copy)

if __name__ == '__main__':
    unittest.main()
