from YNABpy.Support import xmlize

class YNAB3_AccountingWidget:
    """
    Base class for various YNAB3 things
    (ie. YNAB3_Payee, YNAB3_Transaction)

    """

    dom = None

    fields_of_interest = [xmlize('memo'), xmlize('inflow'), xmlize('outflow')]

    def __init__(self, transaction_dom, additional_fields_of_interest):
        """Constructor

        """

        self.dom = transaction_dom

        for field in additional_fields_of_interest:
            if field not in self.fields_of_interest:
                self.fields_of_interest.append(field)

        for child in transaction_dom.childNodes:
            self.load_properties(child)


    def get_property(self, name):
        """ get a property (return None if it doesn't exist)

        We do this because this class loads properties from the xml
        dynamically, so there's a chance some properties may be missing
        """
        if hasattr(self, name):
            return getattr(self, name)
        return None


    def get_inflow(self):
        """ get_inflow
        """
        return self.get_property('inflow')

    def get_outflow(self):
        """ get_outflow
        """
        return self.get_property('outflow')

    def get_balance(self):
        """ get_balance

        Get the balance for this transaction, accounting
        for both outflow and inflow
        """

        if self.get_outflow() != None and self.get_inflow() != None:
            return float(self.get_inflow()) - float(self.get_outflow()) 
        else:
            return None

    def get_memo(self):
        """ get_memo
        """

        return self.get_property('memo')



class YNAB3_Lister:
    """
    YNAB3_Lister base class
    """

    contents = []

    def __init__(self):
        """Constructor
    
        """

        pass 
    
    def get_content(self):
        """ return array of listed objects
        """

        return self.contents

    def add(self, t):
        """ add an item
        """

        self.contents.append(t)

    def get_items_by_text_filter(self, field, filter_str):
        """ Get items that have a argument-supplied property value that 
        matches a substring
        """

        item_list = []

        for item in self.get_content():
            if item.get_property(field) != None:
                if (item.get_property(field).find(filter_str) != -1):
                    item_list.append(item)

        return item_list


