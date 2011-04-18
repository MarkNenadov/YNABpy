"""

Parser.py

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

from xml.dom import minidom

def xmlize(item):
    if sys.version_info[0] == 3:
        return item
    return unicode(item)

class YNAB3_Transaction:
    """
    YNAB3Transaction class

    """

    fields_of_interest = [xmlize('payee'), xmlize('date'), xmlize('accepted'), \
                          xmlize('account'), xmlize('memo'), xmlize('inflow'), \
                          xmlize('outflow')]

    dom = None

    def __init__(self, transaction_dom):
        """Constructor

        """
    
        self.dom = transaction_dom

        for child in transaction_dom.childNodes:
            self.__load_properties(child)

    def __load_properties(self, child):
        """ __load_properties
        Private method to Load ynab transaction properties from a node
        """
        if child.nodeType == child.ELEMENT_NODE:
            if child.hasChildNodes():
                if child.tagName in self.fields_of_interest:
                    for subchild in child.childNodes:
                        if hasattr(subchild, "data"):
                                setattr(self, child.tagName, subchild.data)

    def __get_property(self, name):
        """ get a property (return None if it doesn't exist)

        We do this because this class loads properties from the xml
        dynamically, so there's a chance some properties may be missing
        """
        if hasattr(self, name):
            return getattr(self, name)
        return None

    def get_payee(self):
        """ get_payee
        """
        return self.__get_property('payee')

    def get_date(self):
        """ get_date
        """
        return self.__get_property('date')

    def get_accepted(self):
        """ get_accepted
        """
        return self.__get_property('accepted')

    def get_inflow(self):
        """ get_inflow
        """
        return self.__get_property('inflow')

    def get_outflow(self):
        """ get_outflow
        """
        return self.__get_property('outflow')

    def get_memo(self):
        """ get_memo
        """

        return self.__get_property('memo')

    def get_account(self):
        """ get_account
        """

        return self.__get_property('account')


    def get_xml(self):
        """ return xml 
        """

        return self.dom.toxml()


class YNAB3_Transaction_Lister:
    """
    YNAB3_Transaction_List Class

    """

    contents = []

    def __init__(self):
        """Constructor
    
        """

        pass 
    
    def get_content(self):
        """ return array of transactions
        """

        return self.contents

    def amount(self):
        """ Return # of transactions represented
        """

        return len(self.contents)

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



    def add(self, t):
        """ add a transaction
        """

        self.contents.append(t)


class YNAB3_Parser:
    minidom = None

    """
    YNAB3Parser Class

    """

    def __init__(self, file_path):
        """Constructor

        """

        self.minidom = minidom.parse(file_path)

    def get_transaction_lister(self):
        """ get transaction_liser
        """

        transaction_lister = YNAB3_Transaction_Lister()
        for transactions_node in self.minidom.getElementsByTagName('transactions'):
            for transaction in transactions_node.getElementsByTagName('data.vos.TransactionVO'):
                transaction_lister.add( YNAB3_Transaction(transaction) )
        return transaction_lister

if __name__ == "__main__":
    YNAB_DATA_FILE = "F:/Development/PortableGit/YNABpy/YNABpy/test_budget.ynab3"
    yparser = YNAB3_Parser(YNAB_DATA_FILE)
    transaction_lister = yparser.get_transaction_lister()
    print("# of Payees across the database:")
    print(len(transaction_lister.get_payees()))
    print("Percentage of transactions accepted across the database:")
    print(transaction_lister.get_pct_accepted())
    
