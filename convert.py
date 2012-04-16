# Script to convert CSV to IIF output.

import os
import sys, traceback, re

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


def error(trans):
    sys.stderr.write("%s\n" % trans)
    traceback.print_exc(None, sys.stderr)


def main():
    input_file = open(os.path.join(PROJECT_ROOT, 'input.csv'), 'r')
    output_file = open(os.path.join(PROJECT_ROOT, 'output.iif'), 'w')


    # This is the name of the QuickBooks checking account
    account = "BofA Credit Card"

    # This is the IIF template

    head = "!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	TOPRINT	NAMEISTAXABLE	DUEDATE	TERMS	PAYMETH	SHIPVIA	SHIPDATE	REP	FOB	PONUM	INVMEMO	ADDR1	ADDR2	ADDR3	ADDR4	ADDR5	SADDR1	SADDR2	SADDR3	SADDR4	SADDR5	TOSEND	ISAJE	OTHER1	ACCTTYPE	ACCTSPECIAL\r\n"\
           + "!SPL	SPLID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	QNTY	PRICE	INVITEM	PAYMETH	TAXABLE	EXTRA	VATCODE	VATRATE	VATAMOUNT	VALADJ	SERVICEDATE	TAXCODE	TAXRATE	TAXAMOUNT	TAXITEM	OTHER2	OTHER3	REIMBEXP	ACCTTYPE	ACCTSPECIAL	ITEMTYPE\r\n"\
    + "!ENDTRNS\r\n"

    output_file.write(head)

    template = "TRNS		CREDIT CARD	%s	BofA Credit Card			-%s		%s		N	N	%s																			N			CCARD\r\n"\
               + "SPL		CREDIT CARD	%s	Ask My Accountant			%s				0	%s							0.00					0.00					EXP\r\n"\
    + "ENDTRNS\r\n"


    # And here's the part that inserts data into the tempalate
    for trans in input_file:

        try:
            list = trans.split(',')
            assert (len(list) == 3 )
        except:
            error(trans)
            continue

        try:
            (date, amount, comments) = list
        #            date = date.replace('/', '-')
        except:
            error(trans)
            continue

        try:
            amount = float(amount)
        except:
            error(trans)
            continue

        comments = comments.strip('"')
        comments = comments.strip("\n")
        comments = comments.strip("\r")

        output_file.write(template % (date, amount, comments, date,
                                      date, amount, amount))


if __name__ == '__main__':
    main()