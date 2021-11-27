#!/usr/bin/env python3
"""
Analyse accounts
> python3 accounts.py transactions.csv
"""

from collections import OrderedDict
import decimal
import yaml
import csv
import sys


def headers_data(fn='transactions.csv'):
    f = open(fn, 'r')
    data = list(csv.reader(f))
    f.close()
    return data[0], data


def get_total_income(fn):
    """Quick analysis returning total income for this CSV"""
    headers, data = headers_data(fn)

    total = 0
    for row in data:
        d = dict(zip(headers, row))
        amount = d['Amount']
        if amount[0].isdigit():
            total += decimal.Decimal(row[3])
    return total


def breakdown_per_party(data, headers):
    """Get breakdowns per party from transaction memo"""
    od = OrderedDict()
    # group transactions by 1st part of memo which holds sender/recipient
    for row in data[1:]:
        d = dict(zip(headers, row))
        amount = d['Amount']
        memo = d.get('Memo')
        if not memo:
            memo = d.get('Name')
        if not memo:
            memo = d.get('Description')
        memo_data = [x.strip() for x in memo.split('  ') if x]
        party = memo_data[0]
        # party = ''.join([x for x in party if not x.isdigit()])
        party = party.strip().upper()

        od.setdefault(party, []).append(decimal.Decimal(amount))
    # sum transactions
    results = OrderedDict()
    for party, transcs in od.items():
        results[party] = sum(transcs)
    return sorted(results.items(), key=lambda x: x[1])


def render_breakdowns(fn, threshold=200):
    headers, data = headers_data(fn)
    parties = breakdown_per_party(data, headers)
    revenue, refunds, expenses = [], [], []
    for party in parties:
        name, value = party
        if value < 0:
            expenses.append(party)
        if threshold >= value >= 0:
            refunds.append(party)
        if value > threshold:
            revenue.append(party)

    lines = []
    for category in revenue, expenses, refunds:
        # get variable name
        heading = [k for k, v in locals().items() if v is category][0]
        cat_total = sum(dict(category).values())
        if not cat_total:
            continue
        lines += ['', heading.upper(), '=' * len(heading), '']
        for line in category:
            name, value = line
            col_name = name[:20].rjust(20)
            col_value = str(value).ljust(10)
            lines.append('%s, %s' % (col_name, col_value.rstrip()))
        total_str = 'Total %s (£): %s' % (heading, cat_total)
        lines += ['', total_str, '']

    # tags = ', '.join(dict(expenses).keys())
    return '\n'.join(lines)  # + f'Expense tags: {tags}'


def get_categories(fn='transaction-categories.yml'):
    f = open(fn)
    cats = yaml.safe_load(f)
    f.close()
    cats = {k: sorted(v) for k, v in cats.items()}
    # import json
    # print(json.dumps(cats, indent=4, sort_keys=True))

    lookup = {}
    for cat_name, ls in cats.items():
        for x in ls:
            lookup[x] = cat_name
    return cats, lookup


def expense_categories(fn):
    """Allow user to categorise expenses"""
    headers, data = headers_data(fn)
    breakdowns = breakdown_per_party(data, headers)
    categories, lookup = get_categories()

    totals = OrderedDict()
    for party in breakdowns:
        party_name, amount = party
        party_category = lookup.get(party_name, 'Unknown')
        totals.setdefault(party_category, []).append(amount)

    lines = ['', 'Spending analysis', '=================']
    options = enumerate(categories.keys(), start=1)
    for index, category in options:
        total = sum(totals.get(category, [0]))
        s = '%s) %s: £%s' % (index, category, total)
        lines.append(s)
    lines += ['']
    return '\n'.join(lines)


if __name__ == '__main__':
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 'transactions.csv'

    print(render_breakdowns(fn))
    print(expense_categories(fn))
