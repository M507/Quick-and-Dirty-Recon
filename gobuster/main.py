"""
python3 main.py url.com random

TODO :Add a recursive functionality 


python3 main.py https://url.com/ random-string  <optional list> 

"""
import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/gobuster"
BIN = "/bin/gobuster"
#WORDLIST_TOBEUSED = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
WORDLIST_TOBEUSED = "/usr/share/wordlists/common.txt"
#WORDLIST_TOBEUSED = "/usr/share/wordlists/test.txt"

debug = 1

def work(URL):
    command = BIN + " dir -u "+URL+" -w "+WORDLIST_TOBEUSED+" -o "+TMP_URLs_FILE
    os.system(command)
    return 0

def parse_urls(URL):
    lines_ALL_PATHS = readafile(TMP_URLs_FILE)
    lines_ALL_PATHS = list(dict.fromkeys(lines_ALL_PATHS))
    lines_ALL_URLs = []
    for line in lines_ALL_PATHS:
        found_path = line.split(' ')[0]
        if URL[-1] == "/":
            URL = URL[:-1] 
        lines_ALL_URLs.append(URL + found_path)
    
    overwrite_file(FOUND_URLs_FILE,lines_ALL_URLs)

def arg_main(URL):
    work(URL)
    parse_urls(URL)

if __name__ == "__main__":
    WHOAMI = "HiddenGems/main.py"
    print(WHOAMI+" started")
    if len(sys.argv)  > 2:
        URL    = sys.argv[1]
        RANDOM = sys.argv[2]
        WORDLIST_TOBEUSED_TMP = sys.argv[3]
        try:
            if len(WORDLIST_TOBEUSED_TMP) > 1:
                WORDLIST_TOBEUSED = WORDLIST_TOBEUSED_TMP
        except:
            pass
        try:
            try:
                os.mkdir( PWD + "/Storage/")
            except:
                print(WHOAMI + " Error 1")
            try:
                os.mkdir( PWD + "/Storage/"+RANDOM+"/")
            except:
                print(WHOAMI + " Error 2")
        except:
            print("ERROR _main_ gobuster 3245234")
        VISITED_URLs_FILE   = PWD + "/Storage/"+RANDOM+"/visited_urls.txt"
        FOUND_URLs_FILE     = PWD + "/Storage/"+RANDOM+"/found_urls.txt"
        TMP_URLs_FILE       = PWD + "/Storage/"+RANDOM+"/tmp.txt"
        for file_name in [VISITED_URLs_FILE,FOUND_URLs_FILE,TMP_URLs_FILE]:
            try:
                open(file_name, mode='w').close()
            except OSError:
                print('Failed creating the file')
            else:
                print(file_name+' File created')
        arg_main(URL)
    else:
        print("no args")
