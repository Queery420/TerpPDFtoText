# Cannabis Terpene Data PDF to Text Converter
# Written by Ivy Slick on 6/11/21
# This program uses tabula.py, a PDF text-and-table extraction tool.
# (https://github.com/chezou/tabula-py)
# In order to use tabula, and by extension this program which depends on it,
# tabula and the Java Runtime Environment (JRE) must be installed on the system.
#
# This program extracts terpene table data from Cannabanoid and Terpene Content
# PDFs produced by growers and manufactures operating within the Maryland
# Medical Cannabis Industry and formats it for use in labeling or posting to a
# website.
#
# Code logic
# > Scan program folder for Portable Document Format (PDF) files
# > Extracts Terpene Tables from PDFs into a TXT file (referred to as a "Raw" file)
# > Formats and Prints extracted information to TXT files
# > Organizes TXT files

import os, shutil, tabula, unicodedata

def main ():

# > Set Up Directories
    directory = os.getcwd()
    Text_directory = directory + "/Text Files"
    Raw_directory = directory + "/Raw Files"
    
    if not os.path.exists(Text_directory):
        os.mkdir(Text_directory)
    if not os.path.exists(Raw_directory):
        os.mkdir(Raw_directory)
    
# > Terpene & Prefix Lists
    Terpene_List = ["TOTAL", "Alpha-Pinene", "alpha-Pinene", "beta-Pinene", "beta-Myrcene", "Limonene", "Linalool", "Linolool", "Terpinolene", "Ocimene", "beta-Caryophyllene", "trans-Caryophyllene", "alpha-Humulene", "Fenchol", "alpha-Bisabolol", "Camphene", "alpha-Terpinene", "gamma-Terpinene", "Eucalyptol", "Isopulegol", "Geraniol", "Carene", "cis-Nerolidol", "trans-Nerolidol", "Guaiol", "Caryophyllene oxide", "isopropyltoluene", "Terpineol", "beta-Elemene", "Azulene", "Sabinene", "Borneol", "Cedrol", "Cymene", "Sabinene hydrate", "Fenchone", "Camphor", "Isoborneol", "Menthol", "Pulegone", "Geraniol acetate", "alpha-Cedrene", "Valencene", "beta-Eudesmol"]
    Prefixes = ["Alpha-", "alpha-", "Beta-", "beta-", "Gamma-", "gamma-", "Trans-", "trans-", "Cis-", "cis-"]

# > Core Program Loop
# > > Iterates through all files in the current directory
# > > Identifies all "PDF" files by their extension
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
# > > Attempts to read table data from identified PDFs
# > > > If unsuccessful, will abandon the current PDF and move onto the next file     
            try:
                dfs = tabula.read_pdf(filename, pages="all", stream=True, silent=True)

# > > Creates a TXT "Raw" file with all the information from the PDF
                rfn = "raw_" + str(filename)
                rfn = rfn.replace(".pdf", ".txt")
                r = open(rfn, 'w')
                for line in dfs:
                    r.write(line.to_string())
                r.close()

# > > Reads the data from the Raw file back into the program
                r = open(rfn, 'r')
                cList1 = [line.strip('\n') for line in r]
                r.close()

# > > Verifies the "Raw" TXT has data
                if not cList1:
                    continue

# > > Creates a new TXT file for storing the formatted data
                fn = str(filename)
                fn = fn.replace(".pdf", ".txt")
                f = open(fn, 'w')

# > > A boolean flag for the "Total terpenes" case
                tFlag = True

# > > Reset temporary empty string
                s = ""

# > > Core Scraping Loop
# > > > Formats scraped strings for Dispensary Use
# > > > Each CASE will perform the following functions:
# > > > > a.) Identifies the type of PDF (grower, lab, etc)
# > > > > b.) Searches text for all Terpenes in Terpene_List
# > > > > c.) If it finds a particular terpene, it formats that line, then prints it to the TXT file
# > > > CASE 1 - Holistic Industries Growers (HIG)      
                if cList1[0].__contains__("POTENCY") and not cList1[0].__contains__("TERPENES") and not cList1[0].__contains__("MAX"):
                    f.write("CASE 1: ")
                    for Terpene in Terpene_List:
                        for Line in cList1:
                            tIndex = Line.find(Terpene)
                            a = "-1"
                            if int(tIndex) is not int(a):
                                if tFlag:
                                    s = "TOTAL " + Line[tIndex + 12:tIndex + 17].strip() + "%"
                                    if s.__contains__(" %"):
                                        s = "TOTAL " + Line[tIndex + 5:tIndex + 17].strip() + "%"
                                    f.write(s)
                                    tFlag = False
                                else:
                                    s = Line.strip()
                                    tIndex = Line.find(Terpene)
                                    s = s[tIndex:len(Terpene) + tIndex + 7]
                                    if s.__contains__("n.d.") or s.__contains__("    "):
                                        continue
                                    prefix = ""
                                    for prefix in Prefixes:
                                        if prefix in s:
                                            if prefix == "alpha-" or prefix == "Alpha-":
                                                s = s.replace(prefix, "a")
                                                break
                                            elif prefix == "beta-" or prefix == "Beta-":
                                                s = s.replace(prefix, "b")
                                                break
                                            elif prefix == "gamma-" or prefix == "Gamma-":
                                                s = s.replace(prefix, "g")
                                                break
                                            elif prefix == "trans-" or prefix == "Trans-":
                                                s = s.replace(prefix, "t")
                                                break
                                            elif prefix == "cis-" or prefix == "Cis-":
                                                s = s.replace(prefix, "c")
                                                break
                                    if not s.__contains__("< MRL") and not s.__contains__("n.d."):
                                        s = ", " + s.strip() + "%"
                                        if not s.__contains__("at%"):
                                            f.write(s)
                                break

# > > > CASE 2 - Grow West (GW) & Holistic Industries Growers (HIG)
                elif cList1[0].__contains__("POTENCY"):
                    f.write("CASE 2: ")
                    for Terpene in Terpene_List:
                        for Line in cList1:
                            tIndex = Line.find(Terpene)
                            a = "-1"
                            if int(tIndex) is not int(a):
                                if tFlag:
                                    f.write("TOTAL " + Line[tIndex + len(Terpene):tIndex + len(Terpene) + 5].strip() + "%")
                                    tFlag = False
                                else:
                                    s = Line.strip()
                                    tIndex = Line.find(Terpene)
                                    s = s[tIndex:len(Terpene) + tIndex + 7]
                                    if s.__contains__("n.d.") or s.__contains__("    "):
                                        continue
                                    prefix = ""
                                    for prefix in Prefixes:
                                        if prefix in s:
                                            if prefix == "alpha-" or prefix == "Alpha-":
                                                s = s.replace(prefix, "a")
                                                break
                                            elif prefix == "beta-" or prefix == "Beta-":
                                                s = s.replace(prefix, "b")
                                                break
                                            elif prefix == "gamma-" or prefix == "Gamma-":
                                                s = s.replace(prefix, "g")
                                                break
                                            elif prefix == "trans-" or prefix == "Trans-":
                                                s = s.replace(prefix, "t")
                                                break
                                            elif prefix == "cis-" or prefix == "Cis-":
                                                s = s.replace(prefix, "c")
                                                break
                                    if not s.__contains__("< MRL") and not s.__contains__("n.d."):
                                        f.write(", " + s.strip() + "%")
                                break

# > > > CASE 3
                elif cList1[0].__contains__("SUMMARY"):
                    f.write("CASE 3: ")
                    for Terpene in Terpene_List:
                        for Line in cList1:
                            tIndex = Line.find(Terpene)
                            a = "-1"
                            if int(tIndex) is not int(a):
                                if tFlag:
                                    s = Line[tIndex - 5:tIndex + 5]
                                    f.write(s)
                                    tFlag = False
                                else:
                                    s = ", " + Line[tIndex:len(Terpene) + tIndex + 22].strip()
                                    if s.__contains__("<LOQ") or s.__contains__("ND") or s.__contains__("n.d."):
                                        break
                                    else:
                                        s = s[:len(Terpene) + 2] + " " + s[-5:] + "%"
                                        prefix = ""
                                        for prefix in Prefixes:
                                            if prefix in s:
                                                if prefix == "alpha-" or prefix == "Alpha-":
                                                    s = s.replace(prefix, "a")
                                                    break
                                                elif prefix == "beta-" or prefix == "Beta-":
                                                    s = s.replace(prefix, "b")
                                                    break
                                                elif prefix == "gamma-" or prefix == "Gamma-":
                                                    s = s.replace(prefix, "g")
                                                    break
                                                elif prefix == "trans-" or prefix == "Trans-":
                                                    s = s.replace(prefix, "t")
                                                    break
                                                elif prefix == "cis-" or prefix == "Cis-":
                                                    s = s.replace(prefix, "c")
                                                    break
                                        f.write(s)
                                break

# > > > CASE 4
                elif cList1[0].__contains__("Date Sampled"):
                    f.write("CASE 4: ")
                    for Terpene in Terpene_List:
                        for Line in cList1:
                            tIndex = Line.find(Terpene)
                            a = "-1"
                            if int(tIndex) is not int(a):
                                if tFlag:
                                    s = Line[tIndex - len(Terpene):len(Terpene) + tIndex]
                                    f.write(s)
                                    tFlag = False
                                else:
                                    s = ", " + Line[tIndex:(tIndex + len(Terpene) + 27)]
                                    if s.__contains__("<LOQ") or s.__contains__("ND") or s.__contains__("n.d."):
                                        break
                                    else:
                                        s = s[:len(Terpene) + 2] + " " + s[-5:] + "%"
                                        prefix = ""
                                        for prefix in Prefixes:
                                            if prefix in s:
                                                if prefix == "alpha-" or prefix == "Alpha-":
                                                    s = s.replace(prefix, "a")
                                                    break
                                                elif prefix == "beta-" or prefix == "Beta-":
                                                    s = s.replace(prefix, "b")
                                                    break
                                                elif prefix == "gamma-" or prefix == "Gamma-":
                                                    s = s.replace(prefix, "g")
                                                    break
                                                elif prefix == "trans-" or prefix == "Trans-":
                                                    s = s.replace(prefix, "t")
                                                    break
                                                elif prefix == "cis-" or prefix == "Cis-":
                                                    s = s.replace(prefix, "c")
                                                    break
                                        f.write(s)
                                break

# > > > CASE 5
                else:
                    f.write("CASE 5: ")
                    for Terpene in Terpene_List:
                        for Line in cList1:
                            tIndex = Line.find(Terpene)
                            a = "-1"
                            if int(tIndex) is not int(a):
                                if tFlag:
                                    s = Line[tIndex:len(Terpene) + tIndex] + " " + Line[tIndex + len(Terpene) + 34:tIndex + len(Terpene) + 39] + "%"
                                    f.write(s)
                                    tFlag = False
                                elif Line.__contains__("SUMMARY") or Line == cList1[0]:
                                    continue
                                else:
                                    s = ", " + Line[tIndex:len(Terpene) + tIndex] + " " + Line[tIndex + len(Terpene) + 32:tIndex + len(Terpene) + 37] + "%"
                                    if s.__contains__("<") or s.__contains__(" %") or s.__contains__("D9") or s.__contains__("ND") or s.__contains__("n.d."):
                                        s = ", " + Line[tIndex:len(Terpene) + tIndex] + " " + Line[tIndex + len(Terpene) + 6:tIndex + len(Terpene) + 11] + "%"
                                        if s.__contains__("<") or s.__contains__(" %") or s.__contains__("D9") or s.__contains__("ND") or s.__contains__("n.d."):
                                            continue
                                        else:
                                            prefix = ""
                                            for prefix in Prefixes:
                                                if prefix in s:
                                                    if prefix == "alpha-" or prefix == "Alpha-":
                                                        s = s.replace(prefix, "a")
                                                        break
                                                    elif prefix == "beta-" or prefix == "Beta-":
                                                        s = s.replace(prefix, "b")
                                                        break
                                                    elif prefix == "gamma-" or prefix == "Gamma-":
                                                        s = s.replace(prefix, "g")
                                                        break
                                                    elif prefix == "trans-" or prefix == "Trans-":
                                                        s = s.replace(prefix, "t")
                                                        break
                                                    elif prefix == "cis-" or prefix == "Cis-":
                                                        s = s.replace(prefix, "c")
                                                        break
                                            f.write(s)
                                    else:
                                        prefix = ""
                                        for prefix in Prefixes:
                                            if prefix in s:
                                                if prefix == "alpha-" or prefix == "Alpha-":
                                                    s = s.replace(prefix, "a")
                                                    break
                                                elif prefix == "beta-" or prefix == "Beta-":
                                                    s = s.replace(prefix, "b")
                                                    break
                                                elif prefix == "gamma-" or prefix == "Gamma-":
                                                    s = s.replace(prefix, "g")
                                                    break
                                                elif prefix == "trans-" or prefix == "Trans-":
                                                    s = s.replace(prefix, "t")
                                                    break
                                                elif prefix == "cis-" or prefix == "Cis-":
                                                    s = s.replace(prefix, "c")
                                                    break
                                        f.write(s)
                                break
                            else:
                                continue
                f.close()
                
# > > Moves TXT files into their corresponding directory; deletes Raw files
                shutil.move(os.path.join(directory, fn), os.path.join(Text_directory, fn))
                shutil.move(os.path.join(directory, rfn), os.path.join(Raw_directory, rfn))
                #os.remove(rfn)
                
            except UnicodeEncodeError:
                continue

        else:
            continue

if __name__ == "__main__":
    # execute only if run as a script
    main()
