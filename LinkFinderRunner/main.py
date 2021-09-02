"""
Find URLs in JS files. 
python3 main.py filepath_of_a_file_that_has_js_urls 34nj4io32r

Result:
A file with "hidden" URLs -> found_urls.txt
"""

import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 


PWD = ROOT_DIR + "/LinkFinderRunner"
BIN = ROOT_DIR + "/LinkFinder" + "/linkfinder.py"
SCOPE = PWD + "/Scope/"

# /root/vsvm/LinkFinderRunner/Scope/Blocked_words.txt
BLOCK_LIST_FILE = SCOPE + "Blocked_words.txt"

debug = 1

def work(URL, TMP_FILE):
    # python3 linkfinder.py -i 'https://nd.gea.gov.sa/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js' -o cli
    command = "python3 "+BIN + " -i '" + URL + "' -o cli >> "+TMP_FILE
    print(command)
    os.system(command)
    return 0


def arg_main(URL, RANDOM, VISITED_URLs_FILE, FOUND_URLs_FILE, FOUND_JSs_FILE, TMP_FILE):
    final_lines_ALL_URLs = []
    lines_ALL_URLs_IN_FILE = readafile(IN_FILE)
    lines_ALL_URLs_IN_FILE = list(dict.fromkeys(lines_ALL_URLs_IN_FILE))
    # Clean TMP_FILE
    erase_content_of_file(TMP_FILE)
    for URL in lines_ALL_URLs_IN_FILE:
        try:
            work(URL, TMP_FILE)
            DOMAIN = extract_tld_string(URL)
            try:
                PROTOCOL = URL.split('//')[0] + "//" 
            except:
                print("LinkFinderRunner/main.py arg_main Error 2")
        except:
            print("LinkFinderRunner/main.py arg_main Error 1")
        
        FULL_URL = PROTOCOL + DOMAIN 

        lines_ALL_URLs = readafile(TMP_FILE)
        lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
        for i in range(len(lines_ALL_URLs)):
            if lines_ALL_URLs[i][0] == "/":
                lines_ALL_URLs[i] = lines_ALL_URLs[i][1:]


            if "http://" in lines_ALL_URLs[i]:
                continue
            if "http://" in lines_ALL_URLs[i]:
                continue
            
            lines_ALL_URLs[i] = str(FULL_URL) + "/" + str(lines_ALL_URLs[i])

        final_lines_ALL_URLs = final_lines_ALL_URLs + lines_ALL_URLs
    
    final_lines_ALL_URLs = list(dict.fromkeys(final_lines_ALL_URLs))
    final_lines_ALL_URLs_new = []
    blocked_lines = readafile(BLOCK_LIST_FILE)

    for url in final_lines_ALL_URLs:
        dont_add = 0
        for blocked_word in blocked_lines:
            if blocked_word in url:
                dont_add = 1
        if dont_add == 0:
            final_lines_ALL_URLs_new.append(url)

    overwrite_file(FOUND_URLs_FILE,final_lines_ALL_URLs_new)
    
    return 0

if __name__ == "__main__":
    # python3 main.py filepath_of_a_file_that_has_js_urls 34nj4io32r
    WHOAMI = "LinkFinderRunner/main.py"
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
        except:
            pass
        VISITED_URLs_FILE   = PWD + "/Storage/"+RANDOM+"/visited_urls.txt"
        FOUND_URLs_FILE     = PWD + "/Storage/"+RANDOM+"/found_urls.txt"
        FOUND_JSs_FILE      = PWD + "/Storage/"+RANDOM+"/found_js.txt"
        TMP_FILE            = "/tmp/"+RANDOM+"_LinkFinderRunner.txt"
        for file_name in [VISITED_URLs_FILE,FOUND_URLs_FILE,FOUND_JSs_FILE, TMP_FILE]:
            try:
                open(file_name, mode='w').close()
            except OSError:
                print('Failed creating the file')
            else:
                print(file_name+' File created')
        arg_main(IN_FILE, RANDOM, VISITED_URLs_FILE, FOUND_URLs_FILE, FOUND_JSs_FILE, TMP_FILE)
    else:
        print("no args")
