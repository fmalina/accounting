import unittest
import accounts


test_breakdowns = """
REVENUE
=======

              CLIENT, 999.00    

Total revenue (£): 999.00


EXPENSES
========

       VIRGIN TRAINS, -270.00   
              AIRBNB, -242.00   
                 H3G, -93.20    
         ASDA PETROL, -80.99    
            WORLDPAY, -50.99    
                ALDI, -24.12    
        DON GIOVANNI, -17.98    
           MCDONALDS, -13.18    
                 KFC, -6.39     
              SUBWAY, -4.50     
       PRET A MANGER, -2.35     

Total expenses (£): -805.70
"""


test_spending = """
Spending analysis
=================
1) Accommodation: £-242.00
2) Food: £-44.40
3) Supermarkets: £-24.12
4) Fuel: £-80.99
5) Parking: £0
6) Transport (flights/trains/bus/car rental): £-270.00
7) Income: £999.00
8) Phone: £-93.20
9) Insurance/biz services: £-50.99
10) Other: £0
11) Uncategorised: £0
"""


class TestAccounts(unittest.TestCase):
    fn = 'transactions.csv'

    def test_accounts(self):
        res = accounts.render_breakdowns(self.fn)
        self.assertEqual(res, test_breakdowns)

    def test_spending_analysis(self):
        res = accounts.expense_categories(self.fn)
        self.assertEqual(res, test_spending)


if __name__ == '__main__':
    unittest.main()
