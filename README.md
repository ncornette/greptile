[![Build Status](https://travis-ci.org/ncornette/greptile.svg?branch=master)](https://travis-ci.org/ncornette/greptile) 
[![Codacy Badge](https://api.codacy.com/project/badge/grade/a046f045b39a419b9f31ff1fb324d9a8)](https://www.codacy.com/app/nicolas-cornette/greptile) 

# Greptile
Fast grep implementation in python, with replace features

```
usage: greptile.py [-h] [-v] [-x EXTENSIONS [EXTENSIONS ...]] [-r] [-l] [-i]
                   [-g REPLACE_EXPR] [-f REPLACE_EXPR]
                   expression [file]

file search and replace with regular expressions

positional arguments:
  expression            regular expression
  file                  file path (or directory if -r is used)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -x EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        restrict search to file extensions (ex: .py .txt .java
                        .xml)
  -r, --recursive       recursively search in path
  -l, --list            list files matching pattern
  -i, --inplace         update the file inplace (with -g or -f)
  -g REPLACE_EXPR, --replace-global REPLACE_EXPR
                        global replacement expression
  -f REPLACE_EXPR, --replace-first REPLACE_EXPR
                        first occurrence replacement expression
```

### Why fast?

Because it exclusively uses generators, reptile never allocates big lists, it always processes one line in one file at a time. you can do a search on big files and large directories like `/` recursively without memory overhead.

### Examples: 

#### Search `"import"` in ./greptile.py :
```bash
$ ./greptile.py "import" ./greptile.py
```
```bash
import re
import os
import sys
    import argparse
```

#### Recursively search from `~/` lines in python files containing `Copyright` :
```bash
$ ./greptile.py -x .py -r "Copyright" ~/
```
```bash
/Users/nic/Library/Android/sdk/platform-tools/systrace/systrace-legacy.py 2:  # Copyright (c) 2011 The Chromium Authors. All rights reserved.
/Users/nic/Library/Android/sdk/platform-tools/systrace/systrace.py 2:  # Copyright (c) 2011 The Chromium Authors. All rights reserved.
/Users/nic/Library/Android/sdk/platform-tools/systrace/systrace_agent.py 0:  # Copyright (c) 2015 The Chromium Authors. All rights reserved.
/Users/nic/Library/Android/sdk/platform-tools/systrace/util.py 0:  # Copyright (c) 2015 The Chromium Authors. All rights reserved.
/Users/nic/Library/Android/sdk/platform-tools/systrace/agents/__init__.py 0:  # Copyright (c) 2015 The Chromium Authors. All rights reserved.
/Users/nic/Library/Android/sdk/platform-tools/systrace/agents/atrace_agent.py 0:  # Copyright (c) 2015 The Chromium Authors. All rights reserved.
...
```

#### Replacement & easy grouping with python `re.sub` syntax :
```bash
$ greptile.py "\[(.*)\]\((.*)\)" README.md -g "<a href=\"\2\">\1</a>" | diff -u README.md -
```
```diff
--- README.md	2016-04-19 22:37:20.000000000 +0200
+++ -	2016-04-25 14:54:24.000000000 +0200
@@ -1,4 +1,4 @@
-![Agera](https://github.com/google/agera/blob/master/doc/images/agera.png)
+!<a href="https://github.com/google/agera/blob/master/doc/images/agera.png">Agera</a>
 Reactive Programming for Android
 ================================

```
### Api: 

```python
import greptile

# Replace "import" by "export" from dir `./`, in all files and these extensions: .py, .xml, .java
greptile.replace('import', 'export', './', '.py', '.xml', '.java')

# Return filenames of all files containing the text "import" from dir `./` and .py, .xml, .java
my_list = greptile.grep_rl('import', './', '.py', '.xml', '.java')

# same as calling replace()
greptile.sed_i(my_list, 'import', 'export')

```
