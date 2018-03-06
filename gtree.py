#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# tree.py
#
# Written by Doug Dahms
#
# Prints the tree structure for the path specified on the command line

from os import listdir, sep
from os.path import abspath, basename, isdir

from pyPdf import PdfFileReader

import optparse

# Delimiter
PAGE_DECO_1 = 50
PAGE_DECO_2 = 82
PAGE_DECO_3 = 113
LOC_DECO = 138

LOC_FILE = 'loc.txt'

TOTAL_PAGE_COUNT = 0
DOC_PAGE_COUNT = 0
TOTAL_LOC_INSERTION = 0
TOTAL_LOC_DELETIONS = 0
PC_STR = 'Total Pages count:'
LOC_STR = 'Total Lines count:'


def recur_deli(time, type=0):
    if type == 0:
        return '-'*time
    elif type == 1:
        return ' '*time


def get_loc(filename=LOC_FILE):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def get_page_num(file):
    global TOTAL_PAGE_COUNT
    if file.endswith('.pdf'):
        num = PdfFileReader(open(file, 'rb')).getNumPages()
        TOTAL_PAGE_COUNT += num
        return str(num)
    else:
        return '0'


def tree(dir, padding, print_files=False, isLast=False, isFirst=False,
         locs=None):
    global TOTAL_LOC_INSERTION
    global TOTAL_LOC_DELETIONS
    global DOC_PAGE_COUNT

    if isFirst:
        print padding.decode('utf8')[:-1].encode('utf8') + dir + '\n|'
    else:
        if isLast:
            print padding.decode('utf8')[:-1].encode('utf8') + '\---' + \
                  basename(abspath(dir))
        else:
            print padding.decode('utf8')[:-1].encode('utf8') + '+---' + \
                  basename(abspath(dir))
        if dir.split('/')[-1] in locs:
            # Pull commit message
            s = locs[dir.split('/')[-1]][0]
            # Get title of commit message only
            ss = s.split("  ")[0]
            print padding + recur_deli(9, 1) + '- ' + ss
    if print_files:
        files = listdir(dir)
    else:
        files = [x for x in listdir(dir) if isdir(dir + sep + x)]
    if not isFirst:
        padding += '   '
    files = sorted(files, key=lambda s: s.lower())
    count = 0
    last = len(files) - 1
    for i, file in enumerate(files):
        count += 1
        path = dir + sep + file
        isLast = i == last
        if isdir(path):
            if count == len(files):
                if isFirst:
                    tree(path, padding, print_files, isLast, False, locs)
                else:
                    tree(path, padding + ' ', print_files, isLast, False, locs)
            else:
                tree(path, padding + '|', print_files, isLast, False, locs)
        else:
            page_num = get_page_num(path)
            if isLast:
                l = len(padding) + len(file) + 5
                if file in locs:

                    TOTAL_LOC_INSERTION += int(locs[file][0])
                    TOTAL_LOC_DELETIONS += int(locs[file][1])

                    print padding + '\---' + file + ' ' + \
                        recur_deli(PAGE_DECO_3 - l + 1) + page_num + \
                        recur_deli(LOC_DECO - PAGE_DECO_3 - len(page_num)) + locs[file][0] + \
                        ' insertions(+), ' + locs[file][1].replace('-', '') + \
                        ' deletions(-)'
                    if len(locs[file]) == 3:
                        # Pull commit message
                        s = locs[file][2]
                        # Get title of commit message only
                        ss = s.split("  ")[0]
                        print padding + recur_deli(10, 1) + '- ' + \
                              ss
                    print padding
                else:
                    DOC_PAGE_COUNT += int(page_num)
                    print padding + '\---' + file + ' ' + \
                          recur_deli(PAGE_DECO_3 - l + 1) + page_num
                    print padding
            else:
                l = len(padding) + len(file) + 5
                if file in locs:
                    TOTAL_LOC_INSERTION += int(locs[file][0])
                    TOTAL_LOC_DELETIONS += int(locs[file][1])
                    print padding + '|---' + file + ' ' + \
                        recur_deli(PAGE_DECO_3 - l + 1) + page_num + \
                        recur_deli(LOC_DECO - PAGE_DECO_3 - len(page_num)) + locs[file][0] + \
                        ' insertions(+), ' + locs[file][1].replace('-', '') +\
                        ' deletions(-)'
                    if len(locs[file]) == 3:
                        # Pull commit message
                        s = locs[file][2]
                        # Get title of commit message only
                        ss = s.split("  ")[0]
                        print padding + '|' + recur_deli(9, 1) + \
                              '- ' + ss
                        print padding + '|'
                else:
                    DOC_PAGE_COUNT += int(page_num)
                    print padding + '|---' + file + ' ' + \
                        recur_deli(PAGE_DECO_3 - l + 1) + page_num


def main():
    global TOTAL_LOC_INSERTION
    global TOTAL_LOC_DELETIONS
    global DOC_PAGE_COUNT

    parser = optparse.OptionParser(usage="usage: %prog [options]",
                                   version="%prog 1.0")

    parser.add_option("-p", "--path", dest="path", action='store',
                      help="delivery folder path [default: %default]",
                      metavar="PATH", default='~/Deliver')

    (options, args) = parser.parse_args()
    path = options.path

    locr = get_loc()
    locs = {}
    if isdir(path):
        # print "                                                         " \
        #       "                         [Page count (for documents)]    " \
        #       "   [Line count (for source code)]"
        print "                                            " \
              "[Page count (for documents)]   [Page count (for source code)]" \
              "  [Page count (for both)]  [Line count (for source code)]"

        print "\nFolder PATH listing"
        for line in locr:
            loc = line.split('|')
            if len(loc) == 2:
                locs[loc[0]] = (loc[1],)
            elif len(loc) == 4:
                locs[loc[0]] = (loc[1], loc[2], loc[3])
            else:
                locs[loc[0]] = (loc[1], loc[2])
        tree(path, '', True, False, True, locs)
        print PC_STR + recur_deli(PAGE_DECO_1 - len(PC_STR)) + \
              str(DOC_PAGE_COUNT) + ' pages'
        print PC_STR + recur_deli(PAGE_DECO_2 - len(PC_STR)) + \
              str(TOTAL_PAGE_COUNT - DOC_PAGE_COUNT) + ' pages'
        print PC_STR + recur_deli(PAGE_DECO_3 - len(PC_STR) + 1) + \
              str(TOTAL_PAGE_COUNT) + ' pages'
        print LOC_STR + recur_deli(LOC_DECO - len(LOC_STR) + 1) + \
              str(TOTAL_LOC_INSERTION) + ' insertion(+), ' + \
              str(abs(TOTAL_LOC_DELETIONS)) + ' deletions(-)'
    else:
        print 'ERROR: \'' + path + '\' is not a directory'


if __name__ == '__main__':
    main()
