import sys

def is_py3():
    """ Are we in Python 3?
    """

    return sys.version_info[0] == 3

def xmlize(item):
    """ Do unicode on string if we
    are not in Python 3
    """

    if is_py3():
        return item
    return unicode(item)

