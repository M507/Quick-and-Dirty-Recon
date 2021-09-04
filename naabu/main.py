# naabu -p 21-23,25,53,80,110-111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080 -silent -host hackerone.com
# FM!!!!!!!!!!!!!!!!!!! Don't pusht this \/
"""
python3 /root/vsvm/HiddenGems/main.py https://gggggogle.com RANDOMESTRING

TO RUN THIS YOU NEED TO FOLLOW THIS:

python3 /root/vsvm/naabu/main.py file_path 80,443,8000,8080,8443 RANDOMESTRING
python3 /root/vsvm/naabu/main.py /root/vsvm/Storage/Collected_DNS_Subdomains.txt 80,443,8000,8080,8443 TRY1
"""

import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import *
from threading import Thread

WHOAMI = "HiddenGems/main.py"
PWD = ROOT_DIR + "/naabu"
SCOPE = PWD + "/Scope/"
BIN = "/bin/naabu"

NUM_WORKER_THREADS = 10

debug = 1


def do_work(URL, PORTS, OUT_FILE):
    try:
        URL = re.sub('[^a-zA-Z0-9 \.-]', '', URL)
        # naabu -p 21-23,25,53,80,110-111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080 -silent -host hackerone.com
        command = BIN + " -p "+PORTS+" -silent -host "+URL+" >> "+OUT_FILE
        #print(command)
        os.system(command)
        pass
    except:
        print(WHOAMI+" work Error 312312312")
        return 1
    return 0


def remove_scanned_URLs(URLs, VISITED_DOMAINs_FILE):
    URLs_new = []
    for URL in URLs:
        URL = URL.strip('\n').strip(' ')
        if string_in_large_file(URL,VISITED_DOMAINs_FILE):
            continue
        URLs_new.append(URL)
    return URLs_new

def arg_main(IN_FILE, PORTS, RANDOM, VISITED_DOMAINs_FILE, FOUND_PORTs_FILE, TMP_FILE):
    try:
        file_io = open(IN_FILE,"r")
        while 1:
            URLs = []
            for i in range(NUM_WORKER_THREADS):
                try:
                    URLs.append(file_io.readline())
                except Exception as ex:
                    print(ex)
                    print(WHOAMI+" arg_main Error 5342624")
                    return 1
            
            URLs = [URL for URL in URLs if len(URL) > 1]

            if len(URLs) < 1:
                print(WHOAMI+" empty list .. exiting 5413251")
                break

            print(str(URLs))
            if not URLs:
                break
            
            # Remove scanned URLs
            URLs = remove_scanned_URLs(URLs, VISITED_DOMAINs_FILE)
            if len(URLs) < 1:
                continue

            # create threads
            threads_list = []
            
            for i in range(NUM_WORKER_THREADS):
                try:
                    URL = URLs.pop(0)
                    append_to_file(VISITED_DOMAINs_FILE, URL)
                    th = Thread(target=do_work, args=(URL, PORTS, FOUND_PORTs_FILE))
                    th.start()
                    threads_list.append(th)
                except Exception as ex:
                    print(ex)
                    print(WHOAMI+" arg_main Error 6234683")
                    break

            
            # wait for threads to finish
            for th in threads_list:
                th.join()
            

            print("thread finished...looping")

        file_io.close()
    
    except Exception as ex:
        print(ex)
        print(WHOAMI+" arg_main Error 444565452")
        return 1

    
    return 0


if __name__ == "__main__":
    # python3 main.py filepath 34nj4io32r
    print(WHOAMI + " started")
    if len(sys.argv)  > 2:
        IN_FILE     = sys.argv[1]
        PORTS      = sys.argv[2]
        RANDOM      = sys.argv[3]
        RANDOM      = PORTS.replace(',','_').replace('-','_') + "_" + RANDOM
        init_dirs(PWD, RANDOM, SCOPE)
        VISITED_DOMAINs_FILE   = PWD + "/Storage/"+RANDOM+"/visited_domains.txt"
        FOUND_PORTs_FILE     = PWD + "/Storage/"+RANDOM+"/results.txt"
        TMP_FILE            = "/tmp/"+RANDOM+"_"+WHOAMI+".txt"
        BLOCK_LIST_FILE             = SCOPE + "Blocked_words.txt"
        create_files([VISITED_DOMAINs_FILE,FOUND_PORTs_FILE,TMP_FILE])
        arg_main(IN_FILE, PORTS, RANDOM, VISITED_DOMAINs_FILE, FOUND_PORTs_FILE, TMP_FILE)
        print(WHOAMI+": DONE!")
    else:
        print("no args")
