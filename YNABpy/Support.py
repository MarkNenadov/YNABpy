import sys

TAGS = {}
TAGS['MASTER_CAT'] = 'data.vos.MasterCategoryVO'
TAGS['SUB_CAT'] = 'data.vos.SubCategoryVO'
TAGS['PAYEE'] = 'data.vos.PayeeVO'
TAGS['TRAN'] = 'data.vos.TransactionVO'

def is_py3():
    """ Are we in Python 3?
    """

    return sys.version_info[0] == 3

def is_dom_element(dom):
    """ Is this dom an element?
    """

    if dom.nodeType == dom.ELEMENT_NODE:
        return True
    return False

def xmlize(item):
    """ Do unicode on string if we
    are not in Python 3
    """

    if is_py3():
        return item
    return unicode(item)
