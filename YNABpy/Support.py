import sys

TAGS = {'MASTER_CAT': 'data.vos.MasterCategoryVO', 'SUB_CAT': 'data.vos.SubCategoryVO', 'PAYEE': 'data.vos.PayeeVO',
        'TRAN': 'data.vos.TransactionVO', 'MONTHLY_SUB_CAT_': 'data.vos.MonthlySubCategoryBudgetVO'}


def is_py3() -> bool:
    """ Are we in Python 3?
    """

    return sys.version_info[0] == 3


def is_dom_element(dom) -> bool:
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
