import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 
from threading import Thread


PWD = ROOT_DIR + "/subzy"
VISITED_URLs_FILE = PWD + "/Storage/visited_urls.txt"
BIN = "/root/go/bin/subzy"
WHOAMI = "subzy/main.py"

NUM_WORKER_THREADS = 120
debug = 1

def verify(stdout):
    try:
        FALSE_STRING = "NOT VULNERABLE"
        if FALSE_STRING in stdout:
            return 0 
    except Exception as ex:
            print(ex)
    return 1

def isError(stdout):
    try:
        ERROR_STRING = "ERROR"
        if ERROR_STRING in stdout:
            return 1
    except Exception as ex:
            print(ex)
    return 0

def do_work(target):
    command = BIN + " -target "+ target
    stdout = str(subprocess_execute_command(command))
    
    if debug:
        print(stdout)
    
    if isError(stdout):
        return 0

    if verify(stdout):
        message = PWD + " found something! '" + target + "'"
        slack_notify(message)

    return 1

def main():
    lines_ALL_URLs1 = readafile(ALL_URLs_FILE)
    lines_ALL_URLs2 = readafile(COLLECTED_DNS_SUBDOMAINS)
    lines_ALL_URLs = lines_ALL_URLs1 + lines_ALL_URLs2
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
    lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
    lines_ALL_URLs_new = [ url for url in lines_ALL_URLs if url not in lines_VISITED_URLs]
    #lines_ALL_URLs = prepare_brute_force_list(lines_ALL_URLs_new)
    for line in lines_ALL_URLs:
        try:
            line = line.strip("\r").strip("\n").strip(" ")
            # Needs to be refreshed since somehting new has been added
            lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
            if line in lines_VISITED_URLs:
                continue
            else:
                if len(line) > 1:
                    # Do what u need to do
                    work(line)
                    # Done
                    append_to_file(VISITED_URLs_FILE, line)
        except Exception as ex:
            print(ex)


def main_threaded(IN_FILE):
    # create threads
    threads_list = []
    try:
        file_io = open(IN_FILE,"r")
        while 1:
            URLs = []
            for i in range(NUM_WORKER_THREADS):
                try:
                    URLs.append(file_io.readline())
                except Exception as ex:
                    print(ex)
                    print(WHOAMI+" arg_main Error 52346763")
                    return 1
            
            URLs = [URL for URL in URLs if len(URL) > 1]

            if len(URLs) < 1:
                print(WHOAMI+" empty list .. exiting 3647533756")
                break

            if not URLs:
                break
            
            # Remove scanned URLs
            URLs = remove_scanned_URLs(URLs, VISITED_URLs_FILE)
            if len(URLs) < 1:
                continue

            #print(str(URLs))
            
            for i in range(NUM_WORKER_THREADS):
                try:
                    URL = URLs.pop(0)
                    URL = re.sub('[^a-zA-Z0-9 \.-]', '', URL)
                    append_to_file(VISITED_URLs_FILE, URL)
                    print("Testing "+ URL)
                    th = Thread(target=do_work, args=(str(URL),))
                    th.start()
                    threads_list.append(th)
                except Exception as ex:
                    print(ex)
                    print(WHOAMI+" arg_main Error 34672314")
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

    # wait for threads to finish
    for th in threads_list:
        th.join()

    return 0



if __name__ == "__main__":
    print(WHOAMI+" started")
    for IN_FILE in [ALL_URLs_FILE, COLLECTED_DNS_SUBDOMAINS]:
        main_threaded(IN_FILE)
