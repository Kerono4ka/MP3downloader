# MP3downloader
### This is our first lab. Computer Architecture. Software.

This is small package wich allows you to parse html document with optionally depth
to find links for mp3 files and download them.

You can also create playlist by genre, if you want.

The codestyle of this repository corresponds to pep8 standard (you can check this using
pycodestyle util)

### Run
Just use `python main.py` to see how this package works

### Test
Use `coverage run --source=mp3downloader/,tests/  -m  unittest tests/mp3downloaderTest.py`
to run tests and see code cover with command `cover report`

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| mp3downloader\__init__.py | 1 | 0 | 100% |
| mp3downloader\mp3downloader.py | 114 | 22 | 81% |
| tests\__init__.py | 1 | 0 | 100% |
| tests\mp3downloaderTest.py | 66 | 5 |92% |
| **TOTAL** | **182** | **27** | **85%** |

