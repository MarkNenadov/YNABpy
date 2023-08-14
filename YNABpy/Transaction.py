"""

Transaction.py

INTRODUCTION

YNABpy - A Python module for the YNAB (You Need A Budget) application.

AUTHOR

Mark J. Nenadov (2011)
* Essex, Ontario
* Email: <marknenadov@gmail.com>

LICENSING

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version

This program is distributed in the hope that it will be useful
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import sys

try:
    from YNABpy.Support import xmlize
    from YNABpy.Support import is_dom_element
    from YNABpy.BaseClasses import YNAB3_AccountingWidget
    from YNABpy.BaseClasses import YNAB3_Lister
except ImportError as err:
    print("FATAL ERROR, critical YNAB3py file missing: " + str(err))
    sys.exit()


class YNAB3_Transaction(YNAB3_AccountingWidget):
    """
    YNAB3Transaction class
    
    """

    def __init__(self, transaction_dom):
        """Constructor

        """
        super(YNAB3_Transaction, self).__init__(transaction_dom, [xmlize('accepted'), \
                                                                  xmlize('date'), xmlize('account'),
                                                                  xmlize('accountID'), xmlize('payee'), \
                                                                  xmlize('category'), xmlize('cleared')])

    def load_properties(self, child):
        """ __load_properties
        Private method to Load ynab transaction properties from a node
        """
        if is_dom_element(child):
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

    def get_category(self):
        """ get_category
        """

        return self.get_property('category')

    def get_cleared(self):
        """ get_category
        """

        return self.get_property('cleared')

    def get_accountID(self):
        """ get_accountID
        """

        return self.get_property('accountID')

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
            if transaction.get_account() is not None:
                account_list.append(transaction.get_account())

        # eliminate duplicates
        return list(set(account_list))

    def get_payees(self) -> []:
        """ Get the list of payees represented in this transaction
        lister without duplicates
        """

        payee_list = []
        for transaction in self.contents:
            if transaction.get_payee() is not None:
                payee_list.append(transaction.get_payee())

        # eliminate duplicates
        return list(set(payee_list))

    def __get_transactions_by_text_filter(self, field: str, filter_value: str) -> []:
        """ Get transactions that have a argument-supplied property that
        matches a substring
        """

        transaction_list = []

        for transaction in self.get_content():
            if transaction.get_property(field) != None:
                if (transaction.get_property(field).find(filter_value) != -1):
                    transaction_list.append(transaction)

        return transaction_list

    def get_transactions_by_payee(self, payee_value) -> [YNAB3_Transaction]:
        """ Get transactions that have a payee that matches
        a substring
        """

        return self.get_items_by_text_filter('payee', payee_value)

    def get_transactions_by_memo(self, memo_value: str) -> [YNAB3_Transaction]:
        """ Get transactions that have a memo that matches
        a substring
        """

        return self.get_items_by_text_filter('memo', memo_value)

    def get_transactions_by_category_name(self, category_name) -> [YNAB3_Transaction]:
        """ Get transactions that have a memo that matches
        a substring
        """
        return self.get_items_by_text_filter('category', category_name)

    def get_transactions_by_category(self, category_objs) -> [YNAB3_Transaction]:
        """ Get transactions that have a memo that matches
        a substring
        """

        return self.get_items_by_text_filter('category', category_objs.get_name())

    def get_transactions_by_outflow_filter(self, outflow_filter) -> [YNAB3_Transaction]:
        """
        get transactions that have an outflow that falls inside
        of a tuple in the format of (low number, high number)
        """

        transaction_list = []

        for transaction in self.get_content():
            if transaction.get_outflow() != None:
                if (float(transaction.get_outflow()) >= outflow_filter[0] and float(transaction.get_outflow()) <= outflow_filter[1]):
                    transaction_list.append(transaction)

        return transaction_list

    def get_transactions_by_inflow_filter(self, inflow_filter) -> [YNAB3_Transaction]:
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

    def get_transactions_by_date_filter(self, date_filter) -> [YNAB3_Transaction]:
        """
        get transactions that have an date that falls inside
        of a tuple in the format of (start date, stop date)
        """

        transaction_list = []

        for transaction in self.get_content():
            if transaction.get_date() != None:
                if ((transaction.get_date() <= date_filter[1]) and (transaction.get_date() >= date_filter[0])):
                    transaction_list.append(transaction)
        return transaction_list

    def get_total_inflow(self) -> [int]:
        """ Get total inflow represented in this transaction lister
        """
        inflow = 0

        for transaction in self.get_content():
            inflow += float(transaction.get_inflow())

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
            print(transaction.get_accepted())
            if (transaction.get_accepted() == "true"):
                accepted += 1
            elif (transaction.get_accepted() == "false"):
                not_accepted += 1
        return round(accepted / float(accepted + not_accepted), 2) * 100

    def get_pct_cleared(self):
        """ Get percentage of transactions cleared in this transaction
        lister
        
        """
        cleared = 0
        not_cleared = 0
        for transaction in self.get_content():
            if transaction.get_cleared() == "Cleared":
                cleared += 1
            else:
                not_cleared += 1

        return round(cleared / float(cleared + not_cleared), 2) * 100
