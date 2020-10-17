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

import os
import io
import sys, argparse
import pandas as pd
from lxml import html
import requests


def script_usage():
    print('kaas_data_retrieval.py arguments:')
    print('\n Process and retrieve data from KAAS result URL:')
    print('-o | --output <basename>')
    print('-u | --url <"https://www.genome.jp/kaas-bin/kaas_main?mode=map&id=<run-id>&key=<run-key>">')
    print('Example: kaas_data_retrieval.py --output hsa_hg38 --url "https://www.genome.jp/kaas-bin/kaas_main?mode=map&id=12345678&key=12345678" \n\n')

def urlProcess(outputBasename, url):
    resPage, resTree, resultData = urlBatchProc(url)
    writeOutput(outputBasename, resultData, resPage, resTree)

def urlBatchProc(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    pathways = tree.xpath('//*[@id="main"]/p[5]/a/text()')
#    /html/body/div[3]/p[5]/a
    print(pathways)
    return(page, tree, pathways)

def writeOutput(outputBasename, resultData, resPage, resTree):
    basepath = os.getcwd()
    path = os.path.join(basepath, outputBasename)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    log = os.path.join(basepath, outputBasename, ".log")
    with open(log, 'w') as l:
        print(resTree, file=l)

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
        urlProcess(args.output, args.url)
    else:
        script_usage()
