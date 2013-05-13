# -*- coding: utf-8 -*-

# standard modules
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

# site modules

# local modules
from fracfocustools import FracFocusPDFParser
from fracfocustools import Logger


# CONSTANTS
PROBDIRS = (
            "./data/problem",
           )
TESTDIRS = (
            "./data/format1",
            "./data/format2",
           )

def parse_pdf (filename):
    logger = Logger ()
    f = open(filename, 'rb')
    raw_pdf = f.read()
    f.close()
    parser = FracFocusPDFParser(raw_pdf, logger)
    report = parser.parse_pdf()
    return report, logger

def parse_pdfs(dir):
    print "\n\nParsing PDFs in directory '%s'"%dir
    count = 0
    errcount = 0
    excount = 0
    aucount = 0
    for filenm in os.listdir(dir):
        filepath = os.path.join(dir, filenm)
        if filepath[-4:] != '.pdf': continue
        print "\nParsing:", filepath
        count += 1
        try:
            report, logger = parse_pdf(filepath)
        except Exception as e:
            print "Excpetion:", e
            excount += 1
        print logger.get_messages ()
        #print report.__str__()
        report_str = "%s"%report
        rptpath = filepath + '.tsv'
        f_rpt = open(rptpath, 'w')
        f_rpt.write(report_str)
        f_rpt.close()
        if logger.has_error():
            errcount += 1
        elif report:
            goldpath = rptpath + '.au'
            if os.path.exists(goldpath):
                f_au = open(goldpath)
                gold_str = f_au.read()
                f_au.close()
                if gold_str != report_str:
                    aucount += 1
                    print "Mismatch golden file: %s"%rptpath
            else:
                aucount += 1
                print "Missing golden file: %s"%rptpath

    return count, errcount, excount, aucount

def main():
    # Note: the problems dir is for putting selected debug cases
    #       when working on a problem.  It is usually empty.
    #       When debuging a particular problem, the normal test cases
    #       are ignored.
    total, totalerr, totalexc, totalau = 0, 0, 0, 0
    for dir in PROBDIRS:
        count, errs, excpts, auerrs = parse_pdfs(dir)
        total += count
        totalerr += errs
        totalexc += excpts
        totalau += auerrs
    if count == 0:
        for dir in TESTDIRS:
            count, errs, excpts, auerrs = parse_pdfs(dir)
            print ("Folder %s: %s pdf files: %s errors, %s exceptions, %s au errors."
                   %(dir, count, errs, excpts, auerrs))
            total += count
            totalerr += errs
            totalexc += excpts
            totalau += auerrs
    print ("Parsed %s pdf files: %s errors, %s exceptions, %s au errors."
            %(total, totalerr, totalexc, totalau))

if __name__ == '__main__':
    main()