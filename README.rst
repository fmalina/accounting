Analyse accounts
================
This program takes transaction data CSV file as exported from
Barclays internet banking and produces useful account analysis including income,
expenses, rebates and breakdown of expenses for accounting purposes.

Accepts a CSV file name as an argument, defaulting to transactions.csv

Usage
=====

    python3 accounts.py transactions.csv

Expected CSV headers are as follows (if one starts with different bank's CSV format):

    Number, Date, Account, Amount, Subcategory, Memo