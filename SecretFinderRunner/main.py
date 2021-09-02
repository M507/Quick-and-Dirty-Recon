"""
Find secrets in JS files. 
python3 main.py filepath_of_a_file_that_has_js_urls 34nj4io32r

Result:
A file with possible secrets -> found_secrets.txt
"""

import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 


PWD = ROOT_DIR + "/SecretFinderRunner"
BIN = ROOT_DIR + "/SecretFinder" + "/SecretFinder.py"


debug = 1

def work(URL, TMP_FILE):
    # python3 SecretFinder.py -i 'https://google.com/email-decode.min.js' -o cli
    command = "python3 "+BIN + " -i '" + URL + "' -o cli >> "+TMP_FILE
    print(command)
    os.system(command)
    return 0


def arg_main(IN_FILE, RANDOM, FOUND_SECRETS_FILE, TMP_FILE):
    final_lines_ALL_URLs = []
    lines_ALL_URLs_IN_FILE = readafile(IN_FILE)
    lines_ALL_URLs_IN_FILE = list(dict.fromkeys(lines_ALL_URLs_IN_FILE))
    # Clean TMP_FILE
    erase_content_of_file(TMP_FILE)
    for URL in lines_ALL_URLs_IN_FILE:
        try:
            work(URL, TMP_FILE)
        except:
            print("SecretFinderRunner/main.py arg_main Error 1")
        lines_ALL_URLs = readafile(TMP_FILE)
        final_lines_ALL_URLs = final_lines_ALL_URLs + lines_ALL_URLs
    
    final_lines_ALL_URLs = list(dict.fromkeys(final_lines_ALL_URLs))
    overwrite_file(FOUND_SECRETS_FILE,final_lines_ALL_URLs)
    
    return 0

if __name__ == "__main__":
    # python3 main.py filepath_of_a_file_that_has_js_urls 34nj4io32r
    WHOAMI = "SecretFinderRunner/main.py"
    SCOPE = PWD + "/Scope/"
    print(WHOAMI + " started")
    if len(sys.argv)  > 2:
        IN_FILE     = sys.argv[1]
        RANDOM      = sys.argv[2]
        try:
            try:
                os.mkdir( PWD + "/Storage/")
            except:
                print(WHOAMI + " Error 1")
            try:
                os.mkdir( PWD + "/Storage/"+RANDOM+"/")
            except:
                print(WHOAMI + " Error 2")
            try:
                os.mkdir(SCOPE)
            except:
                print(WHOAMI + " Error 3")
        except:
            pass
        FOUND_SECRETS_FILE  = PWD + "/Storage/"+RANDOM+"/found_secrets.txt"
        TMP_FILE            = "/tmp/"+RANDOM+"_SecretFinderRunner.txt"
        BLOCK_LIST_FILE     = SCOPE + "Blocked_words.txt"
        for file_name in [FOUND_SECRETS_FILE]:
            try:
                open(file_name, mode='w').close()
            except OSError:
                print('Failed creating the file')
            else:
                print(file_name+' File created')
        arg_main(IN_FILE, RANDOM, FOUND_SECRETS_FILE, TMP_FILE)
    else:
        print("no args")
