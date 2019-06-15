import os

IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

def log(message):
    if not IN_AXIS:
        print message
