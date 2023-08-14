"""

BaseClasses.py

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
    from YNABpy.Support import xmlize
except ImportError:
    print("FATAL ERROR, critical YNAB3py file missing: " + str(err))


class YNAB3_AccountingWidget(object):
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

    def toxml(self):
        """ Get XML representation of this objects dom
        """
        return self.dom.toxml()



class YNAB3_Lister(object):
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


