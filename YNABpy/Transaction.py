from YNABpy.Support import xmlize
from YNABpy.BaseClasses import YNAB3_AccountingWidget
from YNABpy.BaseClasses import YNAB3_Lister

class YNAB3_Transaction(YNAB3_AccountingWidget):
    """
    YNAB3Transaction class
    
    """

    fields_of_interest = [xmlize('payee'), xmlize('date'), xmlize('accepted'), \
                          xmlize('account'), xmlize('memo'), xmlize('inflow'), \
                          xmlize('outflow')]


    def __init__(self, transaction_dom):
        """Constructor

        """
        super(YNAB3_Transaction, self).__init__(transaction_dom, [xmlize('accepted'), \
              xmlize('date'), xmlize('account'), xmlize('payee')])

    def load_properties(self, child):
        """ __load_properties
        Private method to Load ynab transaction properties from a node
        """
        if child.nodeType == child.ELEMENT_NODE:
            if child.hasChildNodes():
                if child.tagName in self.fields_of_interest:
                    for subchild in child.childNodes:
                        if hasattr(subchild, "data"):
                                setattr(self, child.tagName, subchild.data)

    def get_payee(self):
        """ get_payee
        """
        return self.get_property('payee')

    def get_date(self):
        """ get_date
        """
        return self.get_property('date')

    def get_accepted(self):
        """ get_accepted
        """
        return self.get_property('accepted')

    def get_account(self):
        """ get_account
        """

        return self.get_property('account')


    def get_xml(self):
        """ return xml 
        """

        return self.dom.toxml()


class YNAB3_Transaction_Lister(YNAB3_Lister):
    """
    YNAB3_Transaction_List Class

    """

    def get_accounts(self):
        """ Get the list of accounts represented in this transaction
        lister without duplicates
        """

        account_list = []
        for transaction in self.contents:
            if transaction.get_account() != None:
                account_list.append(transaction.get_account())

        # eliminate duplicates
        return list(set(account_list))


    def get_payees(self):
        """ Get the list of payees represented in this transaction
        lister without duplicates
        """

        payee_list = []
        for transaction in self.contents:
            if transaction.get_payee() != None:
                payee_list.append(transaction.get_payee())

        # eliminate duplicates
        return list(set(payee_list))

    def __get_transactions_by_text_filter(self, field, filter_str):
        """ Get transactions that have a argument-supplied property that
        matches a substring
        """

        transaction_list = []

        for transaction in self.get_content():
            if transaction.get_property(field) != None:
                if (transaction.get_property(field).find(filter_str) != -1):
                    transaction_list.append(transaction)

        return transaction_list


    def get_transactions_by_payee(self, payee_substr):
        """ Get transactions that have a payee that matches
        a substring
        """

        return self.get_items_by_text_filter('payee', payee_substr)


    def get_transactions_by_memo(self, memo_substr):
        """ Get transactions that have a memo that matches
        a substring
        """

        return self.get_items_by_text_filter('memo', memo_substr)

    def get_transactions_by_outflow_filter(self, outflow_filter):
        """
        get transactions that have an outflow that falls inside
        of a tuple in the format of (low number, high number)
        """

        transaction_list = []

        for transaction in self.get_content():
            if transaction.get_outflow() != None:
                if (float(transaction.get_outflow()) >= outflow_filter[0] and \
                        float(transaction.get_outflow()) <= outflow_filter[1]):
                    transaction_list.append(transaction)

        return transaction_list

    def get_transactions_by_inflow_filter(self, inflow_filter):
        """
        get transactions that have an inflow that falls inside
        of a tuple in the format of (low number, high number)
        """

        transaction_list = []

        for transaction in self.get_content():
            if transaction.get_inflow() != None:
                if (float(transaction.get_inflow()) >= inflow_filter[0] and \
                        float(transaction.get_inflow()) <= inflow_filter[1]):
                    transaction_list.append(transaction)

        return transaction_list



    def get_total_inflow(self):
        """ Get total inflow represented in this transaction lister
        """
        inflow = 0

        for transaction in self.get_content():
            inflow += float(transaction.get_inflow())

        return inflow

    def get_total_outflow(self):
        """ Get total outflow represented in this transaction lister
        """
        outflow = 0

        for transaction in self.get_content():
            outflow += float(transaction.get_outflow())

        return outflow

    def get_pct_accepted(self):
        """ Get percentage of transactions accepted in this transaction
        lister
        
        Note: Technically speaking, accepted + not_accepted may not
        add up to the total amount of transactions (if a transaction
        dom node doesn't have the 'accepted' field)
        """
        accepted = 0
        not_accepted = 0
        for transaction in self.get_content():
            if (transaction.get_accepted() == "true"):
                accepted += 1
            elif (transaction.get_accepted() == "false"):
                not_accepted += 1

        return round(accepted / (accepted + not_accepted), 2) * 100

