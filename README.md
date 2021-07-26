# lovely_logger

#### A logger library which builds on, combines, and simplifies various logging features of Python 3.



lovely_logger is a highly robust, production-ready, feature-rich logger which is used throughout the [Tier2 Technologies](https://www.tier2.tech/) software stack



Why using lovely_logger is better than using the built-in python logging module:

1. It is much easier to use
2. It handles automatic logging of uncaught exception tracebacks
3. It is thread-safe
4. It will flush the log to disk on program crash/exit
5. It handles simultaneous logging to both stdout (the console) and automatically rotating log files by default
6. It supports independent formatters for console vs files out-of-the-box
7. It supports both timezones and milliseconds in the timestamp
8. It has sane defaults, like logging a timestamp in the first place
9. It supports shorthand which makes it just as quick to log as it is to `print()`



##### Getting Started:

```python
import lovely_logger as log # pip install lovely-logger

log.init('filename.log')
log.info('Hello World!')
```

It's that easy!





##### Another Example:

```python
import lovely_logger as log

log.init('./my_log_file.log')

log.debug('here are the in-scope variables right now: %s', dir())
log.info('%s v1.2 HAS STARTED', __file__)
log.warning('here is a warning message')
log.error('generally you would use error for handled exceptions which prevent further execution')
log.critical('generally you would use critical for uncaught exceptions')
```



The `init()` function has more optional parameters:

```python
init(filename, to_console=True, level=DEBUG, max_kb=1024, max_files=5)
```

Setting `to_console` to `False` is useful for windowed applications such as those compiled with `pyinstaller` which have no console.

The valid options for `level` are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL` in that order. setting the level to `ERROR`, for example, will silence your `log.debug()` and `log.warning()` calls while still logging your `log.error()` and `log.critical()` calls.

`max_kb` sets the max logfile size before the log is rotated

`max_files` sets the max number of rotating logs that are to be kept before the oldest is deleted. So, for example, the default `max_kb` of 1024 and `max_files`  of 5 means that up to 5 megabytes of logs will be kept, split among five 1MB files. Once the log reaches 5MB and 1byte, the oldest of the 5 files is rotated away, leaving four 1MB archived log files, and a 1byte active log file



There is another special type of log function that can only be used inside of an exception handler. It will log the full exception traceback for you, (as level=CRITICAL) along with any helpful comments you may have about the exception

```python
try:
    a = 1/0
except:
    log.exception("You can't divide by zero!")
```



because nobody has time to type out complicated words like `exception` or `critical`, and code looks worse when the print statements are all different lengths, there is shorthand here for you.

instead of this:

```python
import lovely_logger as log
log.init('my_log_file.log')

log.debug('This is a debug log entry')
log.info('This is a info log entry')
log.warning('This is a warning log entry')
log.error('This is a error log entry')
log.critical('This is a critical log entry')
try:
    a = 1/0
except:
    log.exception('This is an exception log entry')
```

you can write it like this:

```python
import lovely_logger as log
log.init('my_log_file.log')

log.d('This is a debug log entry')
log.i('This is a info log entry')
log.w('This is a warning log entry')
log.e('This is a error log entry')
log.c('This is a critical log entry')
try:
    a = 1/0
except:
    log.x('This is an exception log entry')
```



By default, the logger is going to output the date/time, level, message, filename, and line number into the log file. It will print all of that same info except the date/time to the console. If you want to override what gets outputted, or change the format, you can manually set the formatting:

```python
import lovely_logger as log

log.FILE_FORMAT = "[%(asctime)s] [%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)"
log.CONSOLE_FORMAT = "[%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)"
log.DATE_FORMAT = '%Y-%m-%d %H:%M:%S.uuu%z'

log.init('my_log_file.log')

log.d('This is a debug log entry')
```



`DATE_FORMAT` follows the formatting of the built in python [time.strftime()](https://docs.python.org/3/library/time.html#time.strftime) with the exception of the "uuu" which was added to support milliseconds

`CONSOLE_FORMAT` and `FILE_FORMAT` follow the formatting from the built in python logging library [LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)

Note that those values must be set before `log.init()` is called.

