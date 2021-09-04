import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 
import threading

LOCK = threading.Lock()
PWD = ROOT_DIR + "/subzy"
VISITED_URLs_FILE = PWD + "/Storage/visited_urls.txt"
BIN = "/root/go/bin/subzy"
WHOAMI = "subzy/main.py"

NUM_WORKER_THREADS = 500
debug = 1


def append_to_file_for_threads(filename, line):
    with LOCK:
        try:
            file1 = open(filename, "a")  # append mode 
            file1.write(line+"\n") 
            file1.close()
            return 0
        except:
            return 1


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

def do_work(URL,VISITED_URLs_FILE):
    if string_in_large_file(URL,VISITED_URLs_FILE):
        #print(URL + " has been tested")
        return 1
    
    print("Testing "+ URL)
    command = BIN + " -target "+ URL
    stdout = str(subprocess_execute_command(command))

    append_to_file_for_threads(VISITED_URLs_FILE, URL)
    
    if debug:
        print(stdout)
    
    if isError(stdout):
        return 1

    if verify(stdout):
        message = PWD + " found something! '" + URL + "'"
        slack_notify(message)

    return 0

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
    return_int = 0
    # create threads
    threads_list = []
    try:
        file_io = open(IN_FILE,"r")
        while 1:
            print("New "+str(NUM_WORKER_THREADS) + " threads")
            URLs = []
            for i in range(NUM_WORKER_THREADS):
                try:
                    URLs.append(file_io.readline())
                except Exception as ex:
                    print(ex)
                    print(WHOAMI+" arg_main Error 52346763")
                    return 1
            
            URLs = [URL for URL in URLs if len(URL) > 1]
            
            #print(str(URLs))

            if len(URLs) < 1:
                print(WHOAMI+" empty list .. exiting 3647533756")
                break

            if not URLs:
                break

            #print(str(URLs))
            
            for i in range(NUM_WORKER_THREADS):
                try:
                    URL = URLs.pop(0)
                    URL = re.sub('[^a-zA-Z0-9 \.-]', '', URL)

                    th = threading.Thread(target=do_work, args=(URL,VISITED_URLs_FILE))
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
        return_int = 1

    # wait for threads to finish
    for th in threads_list:
        th.join()

    return return_int



if __name__ == "__main__":
    print(WHOAMI+" started")
    for IN_FILE in [ALL_URLs_FILE, COLLECTED_DNS_SUBDOMAINS]:
        main_threaded(IN_FILE)
