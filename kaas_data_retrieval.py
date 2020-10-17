#!/usr/bin/env python
#======================================================================
# Bio Bureau Project
#=====================================================================
#
# (/u0254) Copyleft 2020, by Bio Bureau and Contributors.
#
# -----------------
# kaas_data_retrieval
# -----------------
# GNU GPL 2020, by Bio Bureau and Contributors.
#
# ORIGINAL AUTHOR: Giordano Bruno Soares-Souza
# SOURCES AND/OR CONTRIBUTOR(S):
#
# UPDATED BY: Giordano Bruno Soares-Souza
#
# COMMAND LINE: ./kaas_data_retrieval.py -out <output name> -url <kaas result URL>
#
# DEPENDENCIES: lxml, requests
#
#
# DESCRIPTION:
#
# INPUTS: KEGG KAAS URL results
# FUTURE DEVELOPMENTS:
# 1)
################################################################################

from lxml import html
import requests
import os

def script_usage():
    print('kaas_data_retrieval.py arguments:')
    print('\n Process and retrieve data from KAAS result URL:')
    print('-o | --output <basename>')
    print('-u | --url <https://www.genome.jp/kaas-bin/kaas_main?mode=map&id=<run-id>&key=<run-key>>')
    print('Example: kaas_data_retrieval.py --output hsa_hg38 --url https://www.genome.jp/kaas-bin/kaas_main?mode=map&id=12345678&key=12345678')


def urlProcess(outputBasename, url):
    resultData = urlBatchProc(url)
    print('\n\n\n\n\n\n\n\n\n\n\n\nReturn print:')
    print(resultData)
    writeOutput(outputBasename, resultData)

def urlBatchProc(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    pathways = tree.xpath('//*[@id="main"]/p[5]/a/text()')
#    /html/body/div[3]/p[5]/a
    print(pathways)
    return(pathways)

def writeOutput(outputBasename,resultData):
    basepath = os.getcwd()
    path = basepath.join(outputBasename)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='KAAS batch processing',
            description='KAAS (KEGG Automatic Annotation Server) batch download and processing',
            epilog='Dependencies: pyhton3; pandas; lxml; requests; urllib. Run: python3 uniprot_api.py (without any arguments to see usage examples)'
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog) alpha 1.0')
    parser.add_argument('-o', '--output', help='Output basename')
    parser.add_argument('-u', '--url', help='KAAS result URL')
    if len(sys.argv)==1:
        script_usage()
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    if args.output and args.url :
        params = convParameters(args.output, args.url)
        urlProcess(outputBasename, url)
    else:
        script_usage()
