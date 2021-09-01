import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/gobuster"
BIN = "/bin/gobuster"

debug = 1

def work(URL):
    command = BIN + " dir -u "+URL+" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt  -o "+TMP_URLs_FILE
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
    print("subzy/main.py started")
    if len(sys.argv)  > 2:
        URL    = sys.argv[1]
        RANDOM = sys.argv[2]
        os.mkdir( PWD + "/Storage/"+RANDOM)
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
