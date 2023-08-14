"""

MonthlyBudget.py

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
    from YNABpy.Support import TAGS
    from YNABpy.BaseClasses import YNAB3_Lister
    from YNABpy.BaseClasses import YNAB3_AccountingWidget
    from YNABpy.Category import YNAB3_Category
except ImportError as err:
    print("FATAL ERROR, critical YNAB3py file missing: " + str(err))
    sys.exit()


class YNAB3_MonthlyBudget(YNAB3_AccountingWidget, YNAB3_Lister):
    """ YNAB3_MonthlyBudget

    Please note: This class represents the base type MonthlyBudget. 
    MonthlySubCategoryBudgets are represented by the subclass 
    YNAB3_MonthlySubCategoryBudget. 
    """

    def __init__(self, category_dom):
        """ Constructor
        """

        super(YNAB3_MonthlyBudget, self).__init__(category_dom, [xmlize('categoryName'), xmlize('month')])

    def load_properties(self, child):
        """ __load_properties
        Private method to Load ynab category properties from a node
        """

        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName in self.fields_of_interest:
                for subChild in child.childNodes:
                    if hasattr(subChild, "data"):
                        setattr(self, child.tagName, subChild.data)

    def get_children(self, name_filter='') -> []:
        """ Get this Categories child Categories

        (optional argument filters by name)
        """

        children = []

        for child in self.dom.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.tagName == 'monthlySubCategoryBudgets':
                    for subchild in child.childNodes:
                        if is_dom_element(subchild):
                            if subchild.tagName == TAGS['MONTHLY_SUB_CAT_']:
                                # note what we are doing here with 'self',
                                # passing a reference to the subcategories
                                # parent
                                budget = YNAB3_MonthlySubCategoryBudget(subchild, self)
                                children.append(budget)
        return children

    def get_month(self):
        """ get_month
        """

        return self.get_property('month')


class YNAB3_MonthlySubCategoryBudget(YNAB3_Category):
    """ YNAB3_MonthlySubCategoryBudget

    Please note: This class represents a Monthly Sub Category Budget, which is 
    a subclass of YNAB3_MonthlyBudget. 
    """

    parent = None

    def __init__(self, category_dom, parent):
        """ Constructor
        """

        self.parent = parent

        super(YNAB3_MonthlySubCategoryBudget, self).__init__(category_dom, [xmlize('name')])

    def get_name(self):
        """ get_name
        """

        return self.get_property('categoryName')

    def get_parent(self):
        """ Get this SubCategory's parent (ie. the master category)
        """

        return self.parent


class YNAB3_MonthlyBudget_Lister(YNAB3_Lister):
    """
    YNAB3_MonthlyBudget_Lister Class

    """

    def __init__(self):
        self.contents = []
        super(YNAB3_MonthlyBudget_Lister, self).__init__()

    # def get_types(self):
    #    """ Get unique list of category types for this list
    #    of categories
    #    """
    #    
    #    types_list = []

    #    for category in self.contents:
    #        if category.get_type() != None:
    #            types_list.append(category.get_type())

    #    # eliminate duplicates
    #    return list(set(types_list))
