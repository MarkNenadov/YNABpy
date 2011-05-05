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

try:
    from reportlab.pdfgen import canvas
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.units import cm
except ImportError:
    print("The reportlab module is a required for the Reporting parts of YNABpy. Please install that")
    sys.exit(0)

PAGE_CONFIG = {}
PAGE_CONFIG['HEIGHT'] = defaultPageSize[1]
PAGE_CONFIG['WIDTH'] = defaultPageSize[0]

def CM(n):
    """ return a value in centimeters
    """

    return n*cm

class PDFReport:
    """ Represents a YNABpy PDF report
    """
    
    p = None

    def __init__(self, file_name):
        """ Constructor, initialize canvas
        """

        self.p = canvas.Canvas(file_name)
 
    def draw(self):
        """ Draw the PDF
        """

        self.p.rect(CM(0.8),CM(0.8), PAGE_CONFIG['WIDTH']-CM(1.6), \
               PAGE_CONFIG['HEIGHT']-CM(1.6), fill=0)

    def save(self):
        """ Save out the PDF
        """

        self.p.showPage()
        self.p.save()

if __name__ == "__main__":
    pr = PDFReport('test.pdf')
    pr.draw()
    pr.save()
