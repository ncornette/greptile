# greptile
Fast grep implementation in python, with replace features

```
usage: greptile.py [-h] [-v] [-x EXTENSIONS [EXTENSIONS ...]] [-r] [-l] [-i]
                   [-g REPLACE_GLOBAL] [-f REPLACE_FIRST]
                   pattern [file]

file search and replace with regular expressions

positional arguments:
  pattern               regular expression
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
  -g REPLACE_GLOBAL, --replace-global REPLACE_GLOBAL
                        replacement expression
  -f REPLACE_FIRST, --replace-first REPLACE_FIRST
                        replacement expression
```

### Why fast?

Because it exclusively uses generators, reptile never allocates big lists, it always processes one line in one file at a time. you can do a search on big files and large directories like `/`. `reptile.py` without memory overhead.
