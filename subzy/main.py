import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/subzy"
VISITED_URLs_FILE = PWD + "/Storage/visited_urls.txt"
BIN = "/root/go/bin/subzy"

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

def work(target):
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


if __name__ == "__main__":
    print("subzy/main.py started")
    main()
