from YNABpy import Parser

YNAB_DATA_FILE = "F:/Development/PortableGit/YNABpy/YNABpy/test_budget.ynab3"
yparser = Parser.YNAB3_Parser(YNAB_DATA_FILE)
transaction_lister = yparser.get_transaction_lister()
  
    
# test filtering transaction list based on payee substring

print("\nFilter by transactions with payees that match 'Canadian':\n")

for t in transaction_lister.get_transactions_by_payee('Canadian'):
    print( "'" + t.get_payee()  + " ($" + t.get_outflow() + " outflow) ' matches 'Canadian'" )

# test filtering transaction list based on payee memo

print("\nFilter by transactions with payees that match 'immigration':\n")

for t in transaction_lister.get_transactions_by_memo('immigration'):
    print( "'" + t.get_memo() + " ($" + t.get_outflow() + " outflow)' matches 'immigration'" )


# test inflow/outflow filtering

print( "\nTransactions going out that are between $1000 and $9000:" )
for t in transaction_lister.get_transactions_by_outflow_filter([1000, 9000]):
    t_date = "?"

    if t.get_payee() != None:
        t_payee = t.get_payee()

    if t.get_date() != None:
        t_date = t.get_date()

    print(t_payee + " (outflow of $"+str(t.get_outflow())+") on " + t_date + " )")

print( "\nTransactions coming in that are between $1000 and $9000:" )

for t in transaction_lister.get_transactions_by_inflow_filter([1000, 9000]):
    t_date = "?"

    if t.get_payee() != None:
        t_payee = t.get_payee()

    if t.get_date() != None:
        t_date = t.get_date()

    print(t_payee + " (inflow of $"+str(t.get_inflow())+") on " + t_date + " )")