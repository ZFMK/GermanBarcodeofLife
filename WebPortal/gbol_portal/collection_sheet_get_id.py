#!/usr/bin/python
import sys


#from ExcelObjects import *
from openpyxl import Workbook, load_workbook



def readTransactionId (args):
    templateFilepath = args[0];

    #get transactionId
    workbook = load_workbook(templateFilepath)
    transactionId = workbook.properties.subject

    return transactionId


if __name__ == "__main__":


    if len(sys.argv) != 2: 
        sys.exit ('''Get GBOL transaction id from Metadata in Collection Excel Sheet.
    Usage:        {0} "<filename>.xlxs"
    Example:
        {0} documents/download/Sammeltabelle_GBOL_2014-10-14.xlxs
        '''.format(sys.argv[0]))
        
    else:
        args = sys.argv[1:]
        transactionId = readTransactionId(args)
        exit(transactionId)

