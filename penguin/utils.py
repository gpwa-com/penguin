import os
import glob

def is_valid_source(src_arg):
    if os.path.isdir(src_arg):
        return True
    elif os.path.isfile(src_arg):
        _, ext = os.path.splitext(src_arg)
        return ext == '.pdf'
    else:
        return False


def src_as_files(src):
    for src_arg in src:
        if os.path.isdir(src_arg):
            for pdf in glob.iglob(src_arg + os.path.sep + '*.pdf'):
                yield pdf
        elif os.path.isfile(src_arg):
            yield src_arg
