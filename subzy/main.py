import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 

PWD = ROOT_DIR + "/subzy"
VISITED_URLs_FILE = PWD + "/Storage/visited_urls.txt"
BIN = "/root/go/bin/subzy"


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
    
    if isError(stdout):
        return 0

    if verify(stdout):
        message = PWD + " found something!"
        slack_notify(message)

    return 1

def main():
    lines_ALL_URLs_FILE = readafile(ALL_URLs_FILE)
    lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
    for line in lines_ALL_URLs_FILE:
        try:
            line = line.strip("\r").strip("\n").strip(" ")
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
    main()