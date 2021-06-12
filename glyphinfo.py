#!/usr/bin/python
# Simple Python text and image glyphinfo based on PDFlib TET

from sys import argv, version_info
from PDFlib.TET import *

# global option list
globaloptlist = "searchpath={{../data} {../../../resource/cmap}}"

# document-specific option list
docoptlist = ""

# page-specific option list
pageoptlist = "granularity=word"

# Print color space and color value details of a glyph's fill color
def print_color_value(outfp, tet, doc, colorid):

    # We handle only the fill color, but ignore the stroke color.
    # The stroke color can be retrieved analogously with the
    # keyword "stroke".
    colorinfo = tet.get_color_info(doc, colorid, "usage=fill")

    if colorinfo["colorspaceid"] == -1 and colorinfo["patternid"] == -1:
        outfp.write(" (not filled)")
        return

    outfp.write(" (")

    if colorinfo["patternid"] != -1:
        patterntype = tet.pcos_get_number(doc,
                "patterns[%d]/PatternType" % colorinfo["patternid"])

        if patterntype == 1:        # Tiling pattern
            painttype = tet.pcos_get_number(doc,
                 "patterns[%d]/PaintType" % colorinfo["patternid"])
            if painttype == 1:
                outfp.write("colored Pattern)")
                return
            elif painttype == 2:
                outfp.write("uncolored Pattern, base color: ")
                # FALLTHROUGH to colorspaceid output
        elif patterntype == 2:        # Shading pattern
            shadingtype = tet.pcos_get_number(doc,
                 "patterns[%d]/Shading/ShadingType" % colorinfo["patternid"])

            outfp.write("shading Pattern, ShadingType=%d)" % shadingtype)
            return

    csname = tet.pcos_get_string(doc,
                "colorspaces[%d]/name" % colorinfo["colorspaceid"])

    outfp.write(csname)

    # Emit more details depending on the colorspace type
    if csname == "ICCBased":
        iccprofileid = tet.pcos_get_number(doc,
                 "colorspaces[%d]/iccprofileid" % colorinfo["colorspaceid"])

        errormessage = tet.pcos_get_string(doc,
                        "iccprofiles[%d]/errormessage" % iccprofileid);

        # Check whether the embedded profile is damaged
        if len(errormessage) > 0:
            outfp.write(" (%s)" % errormessage)
        else:
            profilename = tet.pcos_get_string(doc,
                    "iccprofiles[%d]/profilename" % iccprofileid);
            outfp.write(" '%s'" % profilename)

            profilecs = tet.pcos_get_string(doc,
                    "iccprofiles[%d]/profilecs" % iccprofileid);
            outfp.write(" '%s'" % profilecs)
    elif csname == "Separation":
        colorantname = tet.pcos_get_string(doc,
                 "colorspaces[%d]/colorantname" % colorinfo["colorspaceid"])
        outfp.write(" '%s'" % colorantname)
    elif csname == "DeviceN":
        outfp.write(" ")

        for i in range(len(colorinfo["components"])):
            colorantname = tet.pcos_get_string(doc,
                    "colorspaces[%d]/colorantnames[%d]" %
                            (colorinfo["colorspaceid"], i))

            outfp.write(colorantname)

            if i != len(colorinfo["components"]) - 1:
                outfp.write("/")
    elif csname == "Indexed":
        baseid = tet.pcos_get_number(doc,
                 "colorspaces[%d]/baseid" % colorinfo["colorspaceid"]);

        csname = tet.pcos_get_string(doc, "colorspaces[%d]/name", baseid);

        outfp.write(" %s" % csname)

    outfp.write(" ")
    for i in range(len(colorinfo["components"])):
        outfp.write("%g" % colorinfo["components"][i])

        if (i != len(colorinfo["components"]) - 1):
            outfp.write("/")
    outfp.write(")")

if len(argv) != 3:
    raise Exception("usage: glyphinfo <infilename> <outfilename>\n")

tet = None
pageno = 0

try:
    tet = TET()

    if version_info >= (3, 0):
        fp = open(argv[2], 'w', 2, 'utf-8')
    else:
        fp = open(argv[2], 'w')
        from ctypes import *
        PyFile_SetEncoding = pythonapi.PyFile_SetEncoding
        PyFile_SetEncoding.argtypes = (py_object, c_char_p)
        PyFile_SetEncoding(fp, 'utf-8')

    tet.set_option(globaloptlist)

    doc = tet.open_document(argv[1], docoptlist)

    if doc == -1:
        raise Exception("Error %d in %s(): %s" % (tet.errnum, tet.apiname, tet.errmsg))

    # get number of pages in the document
    n_pages = tet.pcos_get_number(doc, "length:pages")

    # write UTF-8 BOM
    if version_info >= (3, 0):
        fp.write(u'\ufeff')
    else:
        fp.write("%c%c%c" % (0xef, 0xbb, 0xbf))

    # loop over pages in the document
    for pageno in range(1, int(n_pages) + 1):
        previouscolorid = -1
        page = tet.open_page(doc, pageno, pageoptlist)

        if page == -1:
            print("Error %d in %s(): %s" % (tet.errnum, tet.apiname, tet.errmsg))
            continue                        # try next page

        # Administrative information
        fp.write("[ Document: '%s' ]\n" %
                        tet.pcos_get_string(doc, "filename"))
        fp.write("[ Document options: '%s' ]\n" % docoptlist)
        fp.write("[ Page options: '%s' ]\n" % pageoptlist)
        fp.write("[ ----- Page %d ----- ]\n" % pageno)

        # Retrieve all text fragments
        text = tet.get_text(page)
        while text:
            fp.write("[%s]\n" % text)  # print the retrieved text

            # Loop over all characters
            ci = tet.get_char_info(page)
            while ci:
                # Fetch the font name with pCOS (based on its ID)
                fontname = tet.pcos_get_string(doc, "fonts[%d]/name" % ci["fontid"])

                # Print the Unicode value ...
                fp.write("U+%04X" % ci["uv"])

                # ...and the character itself if it is ASCII 
                if ci["uv"] >= 0x20 and ci["uv"] <= 0x7F:
                    if version_info >= (3, 0):
                        fp.write(" '%s'" % chr(ci["uv"]))
                    else:
                        fp.write(" '%c'" % ci["uv"])
                else:
                    fp.write(" ???")


                # Print font name, size, and position
                fp.write(" %s size=%.2f x=%.2f y=%.2f" %
                    (fontname, ci["fontsize"], ci["x"], ci["y"]))

                # Print the color id
                fp.write(" colorid=%d" % ci["colorid"])

                # Check whether the text color changed
                if ci["colorid"] != previouscolorid:
                    print_color_value(fp, tet, doc, ci["colorid"])
                    previouscolorid = ci["colorid"]

                # Examine the "type" member
                if ci["type"] == TET.CT_SEQ_START:
                    fp.write( " ligature_start")
                elif ci["type"] == TET.CT_SEQ_CONT:
                    fp.write( " ligature_cont")
                # Separators are only inserted for granularity > word
                elif ci["type"] == TET.CT_INSERTED:
                    fp.write( " inserted")

                # Examine the bit flags in the "attributes" member
                if ci["attributes"] != TET.ATTR_NONE:
                    if ci["attributes"] & TET.ATTR_SUB:
                        fp.write("/sub")
                    if ci["attributes"] & TET.ATTR_SUP:
                        fp.write("/sup")
                    if ci["attributes"] & TET.ATTR_DROPCAP:
                        fp.write("/dropcap")
                    if ci["attributes"] & TET.ATTR_SHADOW:
                        fp.write("/shadow")
                    if ci["attributes"] & TET.ATTR_DEHYPHENATION_PRE:
                        fp.write("/dehyphenation_pre")
                    if ci["attributes"] & TET.ATTR_DEHYPHENATION_ARTIFACT:
                        fp.write("/dehyphenation_artifact")
                    if ci["attributes"] & TET.ATTR_DEHYPHENATION_POST:
                        fp.write("/dehyphenation_post")
                    if ci["attributes"] & TET.ATTR_ARTIFACT:
                        fp.write("/Artifact")

                fp.write("\n")
                ci = tet.get_char_info(page)

            fp.write("\n")
            text = tet.get_text(page)

        if tet.get_errnum() != 0:
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
