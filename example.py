import lovely_logger as log # pip install lovely-logger

log.init('example.log')

log.d('This is a debug message')
log.i('This is an info message')
log.w('This is a warning message')
log.e('This is an error message')
log.c('This is a critical message')

try:
    a = 1/0 # you can't divide by zero
except:
    log.x('This is an exception')
    