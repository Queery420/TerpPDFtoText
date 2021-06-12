#!/usr/bin/python
# Simple Python text extractor based on PDFlib TET

from sys import argv, exc_info, version_info
from traceback import print_tb, print_exc
from PDFlib.TET import *

# global option list */
globaloptlist = "searchpath={{../data} {../../../resource/cmap}}"

# document-specific option list */
docoptlist = ""

# page-specific option list */
pageoptlist = "granularity=page"

# separator to emit after each chunk of text. This depends on the
# application's needs; for granularity=word a space character may be useful.
separator = "\n"

if len(argv) != 3:
    raise Exception("usage: extractor <infilename> <outfilename>\n")

tet = None
pageno = 0

try:
    try:

        tet = TET()

        if (version_info[0] < 3):
            fp = open(argv[2], 'w')
        else:
            fp = open(argv[2], 'w', 2, 'utf-8')

        tet.set_option(globaloptlist)

        doc = tet.open_document(argv[1], docoptlist)

        if (doc == -1):
            raise Exception("Error " + repr(tet.get_errnum()) + "in "
                + tet.get_apiname() + "(): " + tet.get_errmsg())

        # get number of pages in the document */
        n_pages = tet.pcos_get_number(doc, "length:pages")

        # loop over pages in the document */
        for pageno in range(1, int(n_pages)+1):
            imageno = -1

            page = tet.open_page(doc, pageno, pageoptlist)

            if (page == -1):
                print("Error " + repr(tet.get_errnum()) + "in "
                    + tet.get_apiname() + "(): " + tet.get_errmsg())
                continue                        # try next page */

            # Retrieve all text fragments; This is actually not required
            # for granularity=page, but must be used for other granularities.
            text = tet.get_text(page)
            while (text != None):
                fp.write(text)  # print the retrieved text

                # print a separator between chunks of text
                fp.write(separator)
                text = tet.get_text(page)

            if (tet.get_errnum() != 0):
                print ("\nError " + repr(tet.get_errnum())
                    + "in " + tet.get_apiname() + "() on page " +
                    repr(pageno) + ": " + tet.get_errmsg() + "\n")

            tet.close_page(page)

        tet.close_document(doc)

    except TETException as ex:
        if pageno == 0:
            print("Error %d in %s(): %s" % (ex.errnum, ex.apiname, ex.errmsg))
        else:
            print("Error %d in %s() on page %d: %s" % (ex.errnum, ex.apiname, pageno, ex.errmsg))

    except Exception as ex:
        print(ex)

finally:
    if tet:
        tet.delete()
