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
# > Extracts Terpene Tables from PDFs
# > Format and Print Found information to TXT files

import os, shutil, tabula

def main ():

    directory = os.getcwd()
    Terpene_directory = directory + "/Text Files"
    if not os.path.exists(Terpene_directory):
        os.mkdir(Terpene_directory)

    Terpene_List = ["TOTAL", "Alpha-Pinene", "beta-Pinene", "beta-Myrcene", "Limonene", "Linalool", "Terpinolene", "Ocimene", "beta-Caryophyllene", "trans-Caryophyllene", "alpha-Humulene", "Fenchol", "alpha-Bisabolol", "Camphene", "alpha-Terpinene", "gamma-Terpinene", "Eucalyptol", "Isopulegol", "Geraniol", "Carene", "cis-Nerolidol", "trans-Nerolidol", "Guaiol", "Caryophyllene oxide", "isopropyltoluene", "alpha-Terpineol", "beta-Elemene", "Azulene", "Sabinene", "Borneol", "Cedrol", "Cymene", "Sabinene hydrate", "Fenchone", "Camphor", "Isoborneol", "Menthol", "Pulegone", "Geraniol acetate", "alpha-Cedrene", "Valencene", "beta-Eudesmol", "Camphene"]

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            try:
                dfs = tabula.read_pdf(filename, pages="all", stream=True)

                rfn = "raw_" + str(filename)
                rfn = rfn.replace(".pdf", ".txt")
                r = open(rfn, 'w')
                for line in dfs:
                    r.write(line.to_string())
                r.close()

                t = open(rfn, 'r')
                cList1 = [line.strip('\n') for line in t]
                t.close()

                # create a TXT file corresponding to the current PDF
                fn = str(filename)
                fn = fn.replace(".pdf", ".txt")
                f = open(fn, 'w')

                tFlag = True
                if cList1[0].__contains__("POTENCY"):
                    for Terpene in Terpene_List:
                        for Line in cList1:
                            tIndex = Line.find(Terpene)
                            a = "-1"
                            if int(tIndex) is not int(a):
                                if tFlag:
                                    f.write(Line[tIndex:len(Terpene) + tIndex + 7].strip() + "%")
                                    tFlag = False
                                else:
                                    s = Line[tIndex:len(Terpene) + tIndex + 7].strip()
                                    if not s.__contains__("< MRL"):
                                        f.write(", " + s.strip() + "%")
                                break
                else:
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
                                    s = ", " + Line[tIndex:len(Terpene) + tIndex + 22].strip()
                                    if s.__contains__("<LOQ") or s.__contains__("ND"):
                                        break
                                    else:
                                        s = s[:len(Terpene) + 2] + " " + s[-5:] + "%"
                                        f.write(s)
                                break

                f.close()
                shutil.move(fn, Terpene_directory)
                os.remove(rfn)

            except:
                continue

            continue

        else:
            continue

if __name__ == "__main__":
    # execute only if run as a script
    main()
