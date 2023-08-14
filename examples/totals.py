# test various total functions (total # payees, total percentage of accepted
# transactions, etc.)

from YNABpy import Parser

YNAB_DATA_FILE = "F:/Development/PortableGit/YNABpy/YNABpy/test_budget.ynab3"
yparser = Parser.YNAB3_Parser(YNAB_DATA_FILE)

transaction_lister = yparser.get_transaction_lister()
print("# of Payees across the database:" + str(len(transaction_lister.get_payees())))
print("# of Accounts across the database:" + str(len(transaction_lister.get_accounts())))
print("Percentage of transactions accepted across the database:" + str(transaction_lister.get_pct_accepted()))
print("Percentage of transactions cleared across the database:" + str(transaction_lister.get_pct_cleared()))
