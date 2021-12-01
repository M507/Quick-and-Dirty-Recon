import sys
ROOT_DIR = "../"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

import sqlite3, os, operator
from collections import OrderedDict

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

"""
Only works on Linux
"""
def getHistoryFileName():
    filePath = "/home/"+BROWSER_USERNAME+"/.config/google-chrome/Default" # user's history database path (Chrome)
    getFiles = os.listdir(filePath)
    historyFile = os.path.join(filePath, 'History')
    newHistoryFile = historyFile+".old"
    return historyFile, newHistoryFile

# Function to extract the domain name from a URL
def parseUrl(url):
    try:
        urlComponents = url.split('//')
        afterHttps = urlComponents[1].split('/', 1)
        domainName = afterHttps[0].replace("www.", "")
        return domainName
    except IndexError:
        print("Error in URL")

# Function to return the history database location
def getHistoryFile():
    historyFile, newHistoryFile = getHistoryFileName()
    os.system("cp "+historyFile+" "+ newHistoryFile)
    return newHistoryFile

# Function to query on the database file
def queryHistoryFile(historyFile):
    c = sqlite3.connect(historyFile)
    cursor = c.cursor()
    query = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def writelines_intofile(lines):
    f = open("/tmp/.sdfbhdkslqf.txt", "w")
    f.writelines(lines)
    f.close()

def get_domains():
    #code execution starts here
    historyFile = getHistoryFile()
    queryResults = queryHistoryFile(historyFile)
    URLs = [(url[0]) for url in queryResults]
    URLs = [(str(urlparse(url).hostname)+'\n') for url in URLs]
    URLs = list(dict.fromkeys(URLs))
    for url in URLs:
        print(url)
    historyFile, newHistoryFile = getHistoryFileName()
    os.remove(newHistoryFile)
    return URLs


def get_urls():
    URLs = []
    try:
        historyFile = getHistoryFile()
        queryResults = queryHistoryFile(historyFile)
        for line in queryResults:
            URLs.append(line[0]+"\n")
    except:
        print("Error get_urls()")
    return URLs

def send_urls_to_vsvm():
    try:
        queryResults = get_urls()
        writelines_intofile(queryResults)
        command = "cat /tmp/.sdfbhdkslqf.txt |  ssh root@vsvm.mohammed.red -T 'cat >> /root/vsvm/Storage/urls_with_parameters.txt'"
        os.system(command)
        slack_notify("Chrome has sent today's full urls to VSMV.mohammed.red")
    except:
        print("Error get_urls()")

def send_hostnames():
    try:
        queryResults = get_domains()
        writelines_intofile(queryResults)
        command = "cat /tmp/.sdfbhdkslqf.txt |  ssh root@vsvm.mohammed.red -T 'cat >> /root/vsvm/Storage/urls.txt'"
        os.system(command)
        slack_notify("Chrome has sent today's data to VSMV.mohammed.red")
    except:
        slack_notify("VSMV: Send-urls.py faced an error!!")


send_hostnames()
