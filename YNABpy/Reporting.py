"""

Reporting.py

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

from YNABpy.Transaction import YNAB3_Transaction_Lister
from YNABpy.Category import YNAB3_Category_Lister
from YNABpy.MonthlyBudget import YNAB3_MonthlyBudget_Lister
from YNABpy.Payee import YNAB3_Payee_Lister

try:
    from reportlab.pdfgen import canvas
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.units import cm
except ImportError:
    print("The reportlab module is a required for the Reporting parts of YNABpy. Please install that")
    sys.exit(0)

PAGE_CONFIG = {'HEIGHT': defaultPageSize[1], 'WIDTH': defaultPageSize[0]}


def CM(n) -> int:
    """ return a value in centimeters
    """

    return n * cm


class PDFReport:
    """ Represents a YNABpy PDF report
    """

    c = None
    lister = None
    lister_type = None

    def __init__(self, file_name: str):
        """ Constructor, initialize canvas
        """

        self.c = canvas.Canvas(file_name)

    def link2lister(self, lister):
        self.lister = lister
        if self.lister.__class__ == YNAB3_Transaction_Lister:
            self.lister_type = 'Transaction'
        elif self.lister.__class__ == YNAB3_Category_Lister:
            self.lister_type = 'Category'
        elif self.lister.__class__ == YNAB3_MonthlyBudget_Lister:
            self.lister_type = 'MonthlyBudget'
        elif self.lister.__class__ == YNAB3_Payee_Lister:
            self.lister_type = 'Payee'

    def draw(self):
        """ Draw the PDF
        """

        # draw rectange outline of the PDF

        self.c.rect(CM(0.8), CM(0.8), PAGE_CONFIG['WIDTH'] - CM(1.6), PAGE_CONFIG['HEIGHT'] - CM(1.6), fill=0)

        if self.lister is not None:
            if self.lister_type == "Transaction":
                data_columns = ["Date", "Payee", "Account", "Balance", "Memo"]
                data_values = []
                for trans in self.lister.get_content():
                    data_values.append([trans.get_date(), trans.get_payee(), trans.get_account(), trans.get_balance(), trans.get_memo()])

        self.c.rect(CM(0.8), CM(0.8), PAGE_CONFIG['WIDTH'] - CM(1.6), PAGE_CONFIG['HEIGHT'] - CM(1.6), fill=0)
        self.c.setFont("Helvetica", 18)
        self.c.drawCentredString(PAGE_CONFIG['WIDTH'] / 2.0, PAGE_CONFIG['HEIGHT'] - CM(2.0),
                                 "YNABpy Report on Transactions")

    def save(self) -> None:
        """ Save out the PDF
        """

        self.c.showPage()
        self.c.save()


if __name__ == "__main__":
    pr = PDFReport('test.pdf')
    pr.draw()
    pr.save()
