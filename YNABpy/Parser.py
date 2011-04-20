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

try:
    from xml.dom import minidom
except ImportError:
    print("FATAL ERROR: Can't import xml.dom.minidom!")

try:
    from Payee import YNAB3_Payee_Lister
    from Payee import YNAB3_Payee
    from Category import YNAB3_Category_Lister
    from Category import YNAB3_Category
    from Transaction import YNAB3_Transaction_Lister
    from Transaction import YNAB3_Transaction

except ImportError as err:
    print("FATAL ERROR: " + str(err))

class YNAB3_Parser:
    minidom = None

    """
    YNAB3Parser Class

    """

    def __init__(self, file_path):
        """Constructor

        """

        self.minidom = minidom.parse(file_path)

    def get_payee_lister(self):
        """ get_payee_lister
        """

        payee_lister = YNAB3_Payee_Lister()
        for payee_node in self.minidom.getElementsByTagName('payees'):
            for p in payee_node.getElementsByTagName('data.vos.PayeeVO'):
                payee_lister.add( YNAB3_Payee(p) )
        return payee_lister

    def get_category_lister(self):
        """ get_category_lister
        """
        category_lister = YNAB3_Category_Lister()
        for category_node in self.minidom.getElementsByTagName('categories'):
            for c in category_node.getElementsByTagName('data.vos.MasterCategoryVO'):
                category_lister.add( YNAB3_Category(c) )
        return category_lister

    def get_transaction_lister(self):
        """ get_transaction_lister
        """

        transaction_lister = YNAB3_Transaction_Lister()
        for transactions_node in self.minidom.getElementsByTagName('transactions'):
            for transaction in transactions_node.getElementsByTagName('data.vos.TransactionVO'):
                transaction_lister.add( YNAB3_Transaction(transaction) )
        return transaction_lister

if __name__ == "__main__":

    print("This is a module meant for being imported. Please refer to examples in the project folder!")

   
    YNAB_DATA_FILE = "F:/Development/PortableGit/YNABpy/YNABpy/test_budget.ynab3"
    yparser = YNAB3_Parser(YNAB_DATA_FILE)

    #payee_lister = yparser.get_payee_lister()
    #for x in payee_lister.get_payees_by_name("Mark"):
    #   print( x.get_name() )

    category_lister = yparser.get_category_lister()
    print( category_lister.get_types())
    for c in category_lister.get_content():
        print( "Cat: " + c.get_name())
        for x in c.get_children():
            print( "Subcat: " + x.get_name() )
        print( "yahoo" )
