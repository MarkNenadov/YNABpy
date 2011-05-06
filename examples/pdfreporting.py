from YNABpy import Parser
from YNABpy import Reporting

YNAB_DATA_FILE = "F:/Development/PortableGit/YNABpy/YNABpy/test_budget.ynab3"
yparser = Parser.YNAB3_Parser(YNAB_DATA_FILE)

transaction_lister = yparser.get_transaction_lister()
pdfreport = Reporting.PDFReport("report.pdf")
pdfreport.link2lister(transaction_lister)
pdfreport.draw()
pdfreport.save()
