# Loggify: capture prints and tracebacks to a log file with 2&nbsp;lines of code

[![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/loggify?color=1)](https://pypi.org/project/loggify/)
[![license](https://img.shields.io/pypi/l/loggify)](https://github.com/ar-nowaczynski/loggify)

Loggify is a convenient way to redirect stdout and stderr to the timestamped log file. It works by temporarily overriding the default behaviour of `sys.stdout` and `sys.stderr` in the context manager. You still see the output in the console - it is just additionally streamed to the log file (see the example below).

## Installation

```bash
$ pip install loggify
```

## Usage

script.py:

```python
from loggify import Loggify

def main():
    print("START")
    for i in range(10):
        print(" " * i + "x")
    print("END")
    5 / 0   # traceback will be captured

with Loggify("main.log"):  # specify output filename
    main()
```

main.log:
```
2020-04-07 20:45:18.391:STDOUT:START
2020-04-07 20:45:18.391:STDOUT:x
2020-04-07 20:45:18.391:STDOUT: x
2020-04-07 20:45:18.391:STDOUT:  x
2020-04-07 20:45:18.391:STDOUT:   x
2020-04-07 20:45:18.391:STDOUT:    x
2020-04-07 20:45:18.391:STDOUT:     x
2020-04-07 20:45:18.391:STDOUT:      x
2020-04-07 20:45:18.391:STDOUT:       x
2020-04-07 20:45:18.391:STDOUT:        x
2020-04-07 20:45:18.391:STDOUT:         x
2020-04-07 20:45:18.392:STDOUT:END
2020-04-07 20:45:18.392:STDERR:Traceback (most recent call last):
2020-04-07 20:45:18.392:STDERR:  File "script.py", line 11, in <module>
2020-04-07 20:45:18.392:STDERR:    main()
2020-04-07 20:45:18.392:STDERR:  File "script.py", line 8, in main
2020-04-07 20:45:18.392:STDERR:    5 / 0   # traceback will be captured
2020-04-07 20:45:18.392:STDERR:ZeroDivisionError: division by zero
```

## License

MIT License (see [LICENSE](https://github.com/ar-nowaczynski/loggify/blob/master/LICENSE)).
