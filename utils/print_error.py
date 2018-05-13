import inspect


def print_error(e, error_string):
    # 0 represents this line
    # 1 represents line at caller
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)

    print("{}: {}\nFile: \"{}\", line: {}, in {}"
          .format(error_string, e, info.filename, info.lineno, info.function))
