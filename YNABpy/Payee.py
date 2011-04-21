
try:
    from YNABpy.Support import xmlize
    from YNABpy.Support import is_dom_element
    from YNABpy.BaseClasses import YNAB3_Lister
    from YNABpy.BaseClasses import YNAB3_AccountingWidget
except ImportError as err:
    print("FATAL ERROR, critical YNAB3py file missing: " + str(err)    

class YNAB3_Payee(YNAB3_AccountingWidget):
    """
    YNAB3Transaction class

    """

    name = ""

    def __init__(self, payee_dom):
        """Constructor

        """
        
        super(YNAB3_Payee, self).__init__(payee_dom, [xmlize('category')])


    def load_properties(self, child):
        """ __load_properties
        Private method to Load ynab payee properties from a node
        """
        if is_dom_element(child):
            if child.hasChildNodes():
                if child.nodeName == "name":
                    for subchild in child.childNodes:
                        self.name = subchild.data
                elif child.nodeName == "autoFillData":
                    for subchild in child.childNodes:
                        if not hasattr(subchild, "data"):        
                            for subsubchild in subchild.childNodes:
                                if hasattr(subsubchild, "data"):
                                    setattr(self, subchild.tagName, subsubchild.data)

    def get_category(self):
        """ get_memo
        """

        return self.get_property('category')

    def get_name(self):
        """ get_name
        """

        return self.get_property('name')



class YNAB3_Payee_Lister(YNAB3_Lister):
    """
    YNAB3_Payee_Lister

    """

    def get_categories(self):
        """ Get a unique list of categories for this list of
        payees
        """

        category_list = []

        for payee in self.contents:
            if payee.get_category() != None:
                category_list.append(payee.get_category())

        # eliminate duplicates
        return list(set(category_list))

    def get_payees_by_memo(self, memo_substr):
        """ Get transactions that have a memo that matches
        a substring
        """

        return self.get_items_by_text_filter('memo', memo_substr)

    def get_payees_by_name(self, name_substr):
        """ Get transactions that have a name that matches
        a substring
        """

        return self.get_items_by_text_filter('name', name_substr)


    def get_payees_by_category(self, category_substr):
        """ Get transactions that have a category that matches
        a substring
        """

        return self.get_items_by_text_filter('category', category_substr)


