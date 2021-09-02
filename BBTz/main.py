"""
Find JS files using a file of URLs

# python3 main.py filepath reffg45tg34tg3

Result:
https://kkkkkkkkkkkka.com/jquery.js
https://kkkkkkkkkkkka.com/nd.js
https://www.googletagmanager.com/gtag/js?id=UA-3e302-2
https://kkkkkkkkkkkka/cdn-cgi/scripts/33/cloudflare-static/email-decode.min.js

"""

import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 


PWD = ROOT_DIR + "/BBTz"
BIN = PWD + "/getsrc.py"

debug = 1

def work(URL, FOUND_JSs_FILE):
    # python3 getsrc.py http://10.10.1.5/
    try:
        command = "python3 "+BIN + " '" + URL + "' >> "+FOUND_JSs_FILE
        print(command)
        os.system(command)
    except Exception as e:
        print(e)
        print(BIN+" Error 7563723")
    return 0


def arg_main(IN_FILE, RANDOM, VISITED_URLs_FILE, FOUND_URLs_FILE, FOUND_JSs_FILE):
    lines_ALL_URLs = readafile(IN_FILE)
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))

    for URL in lines_ALL_URLs:
        try:
            work(URL, FOUND_JSs_FILE)
        except:
            print("Error at arg_main()")
    
    lines_ALL_URLs = readafile(FOUND_JSs_FILE)
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))

    # remove unwated lines like errors
    # HTTPSConnectionPool
    blocked_words = readafile(BLOCK_LIST_FILE)
    blocked_words = list(dict.fromkeys(blocked_words))
    
    for url_tmp in lines_ALL_URLs:
        remove_url = 0
        for blocked_word in blocked_words:
            if blocked_word in url_tmp:
                remove_url = 1
        if remove_url:
            lines_ALL_URLs.remove(url_tmp)

    overwrite_file(FOUND_JSs_FILE,lines_ALL_URLs)
    
    return 0

if __name__ == "__main__":
    # python3 main.py filepath reffg45tg34tg3
    WHOAMI = "BBTz/main.py"
    print(WHOAMI+" started")
    if len(sys.argv)  > 2:
        IN_FILE    = sys.argv[1]
        RANDOM = sys.argv[2]
        SCOPE = PWD + "/Scope/"
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
        VISITED_URLs_FILE   = PWD + "/Storage/"+RANDOM+"/visited_urls.txt"
        FOUND_URLs_FILE     = PWD + "/Storage/"+RANDOM+"/found_urls.txt"
        FOUND_JSs_FILE      = PWD + "/Storage/"+RANDOM+"/found_js.txt"
        BLOCK_LIST_FILE     = SCOPE + "Blocked_words.txt"
        for file_name in [VISITED_URLs_FILE,FOUND_URLs_FILE,FOUND_JSs_FILE]:
            try:
                open(file_name, mode='w').close()
            except OSError:
                print('Failed creating the file')
            else:
                print(file_name+' File created')
        arg_main(IN_FILE, RANDOM, VISITED_URLs_FILE, FOUND_URLs_FILE, FOUND_JSs_FILE)
    else:
        print("no args")
