import os

IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

NO_LOGGING = os.environ.has_key("NO_LOGGING")

def log(message):
    if not IN_AXIS and not NO_LOGGING:
        print message
