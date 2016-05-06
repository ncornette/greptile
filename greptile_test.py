#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def test_matching_lines(self):
        self.assertEqual([
            (39, 'Application, but excluding the System Libraries of the Combined Work.\n'),
            (127, '  5. Combined Libraries.\n')
        ],
                [l for l in greptile._matching_lines(re.compile('Libraries'), './test/LICENSE.txt')])

    def test_matching_sed(self):
        sio = io.StringIO()
        with open('./test/LICENSE.txt', 'r') as f:
            greptile.sed(f, 'Material', 'Spam', sio)

        with open('./test/LICENSE.txt', 'r') as f:
            self.assertEqual([
                '-  3. Object Code Incorporating Material from Library Header Files.\n',
                '+  3. Object Code Incorporating Spam from Library Header Files.\n'],
                 [l for l in difflib.unified_diff(f.readlines(), sio.getvalue().splitlines(1))][6:8])


if __name__ == '__main__':
    unittest.main()
