"""

Category.py

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
    from YNABpy.Support import is_dom_element
    from YNABpy.Support import TAGS
    from YNABpy.BaseClasses import YNAB3_Lister
    from YNABpy.BaseClasses import YNAB3_AccountingWidget
except ImportError:
    print("FATAL ERROR, critical YNAB3py file missing: " + str(err))

class YNAB3_Category(YNAB3_AccountingWidget, YNAB3_Lister):
    """ YNAB3_Category

    Please note: This class represents the base type Category. Sub Categories
    are represented by the subclass YNAB3_SubCategory. One difference would be
    that in the YNAB database Categories have a type, but SubCategories don't.
    For our purposes, we also pass a reference to the parent object to a Sub 
    Category but not to a Category.
    """

    def __init__(self, category_dom):
        """ Constructor
        """
        
        super(YNAB3_Category, self).__init__(category_dom, \
                [xmlize('name'),  xmlize('type'), xmlize('note')])


    def load_properties(self, child):
        """ __load_properties
        Private method to Load ynab category properties from a node
        """

        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName in self.fields_of_interest:
                for subchild in child.childNodes:
                    if hasattr(subchild, "data"):
                        setattr(self, child.tagName, subchild.data)

    def get_children(self, name_filter=''):
        """ Get this Categories child Categories

        (optional argument filters by name)
        """

        children = []

        for child in self.dom.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.tagName == 'subCategories':
                    for subchild in child.childNodes:
                        if is_dom_element(subchild):
                            if subchild.tagName == TAGS['SUB_CAT']:
                                # note what we are doing here with 'self',
                                # passing a reference to the subcategories
                                # parent
                                category = YNAB3_SubCategory(subchild, self)
                                if category.get_name().find(name_filter) != -1:
                                    children.append(category)
        return children
        

    def get_name(self):
        """ get_name
        """

        return self.get_property('name')

    def get_type(self):
        """ get_name
        """

        return self.get_property('type')

class YNAB3_SubCategory(YNAB3_Category):
    """ YNAB3_Category

    Please note: This class represents a Sub Category, which is a subclass of
    YNAB3_Category. One difference would be that in the YNAB database Categories 
    have a type, but SubCategories don't. For our purposes, we also pass a reference 
    to the parent object to a Sub Category but not to a Category.
    """

    parent = None

    def __init__(self, category_dom, parent):
        """ Constructor
        """

        self.parent = parent

        super(YNAB3_Category, self).__init__(category_dom, \
                [xmlize('name'),  xmlize('note')])


    def get_parent(self):
        """ Get this SubCategory's parent (ie. the master category)
        """

        return self.parent


class YNAB3_Category_Lister(YNAB3_Lister):
    """
    YNAB3_Category_Lister Class

    """

    def __init__(self):
        self.contents = []
        super(YNAB3_Category_Lister, self).__init__()

    def get_types(self):
        """ Get unique list of category types for this list
        of categories
        """
        
        types_list = []

        for category in self.contents:
            if category.get_type() != None:
                types_list.append(category.get_type())

        # eliminate duplicates
        return list(set(types_list))

