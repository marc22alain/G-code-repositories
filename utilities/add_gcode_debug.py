import os

def addDebug(frame):
    '''Generates a debug statement formatted to add to g-code.'''
    file_text = ''
    if 'DEBUG_GCODE' in os.environ.keys():
        trace = inspect.getframeinfo(frame)
        class_file = trace.filename.split('/')[-1].split('_class')[0]
        file_text = G.comment(\
            '# %s' % (class_file + '.' + trace.function + ' - line:' + str(trace.lineno)))
    return file_text
