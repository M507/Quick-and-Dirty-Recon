import sys
import itertools
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/subdomain-enumeration-2019"
SE2019_STORAGE = PWD + "/Storage/"
VISITED_URLs_FILE = PWD + "/Storage/visited_urls.txt"
STAFE_0_FILE = PWD + "/Storage/stage0.txt"
STAFE_1_FILE = PWD + "/Storage/stage1.txt"
STAFE_2_FILE = PWD + "/Storage/stage2.txt"
STAFE_3_FILE = PWD + "/Storage/stage3.txt"
STAFE_4_FILE = PWD + "/Storage/stage4.txt"
STAFE_5_FILE = PWD + "/Storage/stage5.txt"
SE2019_BLOCKLIST = SE2019_STORAGE + "/blocklist.txt"

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

def clean():
    # Clean
    command = "rm "+SE2019_STORAGE+ "/stage* "
    os.system(command)

    command = "cd "+SE2019_STORAGE+ "; touch stage2.txt stage3.txt stage4.txt stage1.txt stage0.txt stage5.txt"
    os.system(command)


def work():

    BIN_MASSDNS = ROOT_DIR + "/massdns"                     + "/main.py"
    BIN_AMASS   = ROOT_DIR + "/Amass"                       + "/main.py"
    BIN_commonspeak2  = ROOT_DIR + "/commonspeak2-wordlists"      + "/main.py"
    BIN_ALTDNS  = ROOT_DIR + "/altdns"                      + "/main.py"


    command = "python3 " + BIN_AMASS + " "+ STAFE_0_FILE + " "+ STAFE_1_FILE
    print(command)
    os.system(command)

    command = "python3 " + BIN_MASSDNS + " "+ STAFE_1_FILE + " "+ STAFE_2_FILE
    print(command)
    os.system(command)
    valid_domains = readafile(STAFE_2_FILE)
    append_to_file_lines(STAFE_5_FILE, valid_domains)

    command = "python3 " + BIN_commonspeak2 + " "+ STAFE_0_FILE + " "+ STAFE_1_FILE
    print(command)
    os.system(command)

    command = "python3 " + BIN_MASSDNS + " "+ STAFE_1_FILE + " "+ STAFE_2_FILE
    print(command)
    os.system(command)
    valid_domains = readafile(STAFE_2_FILE)
    append_to_file_lines(STAFE_5_FILE, valid_domains)

    command = "python3 " + BIN_ALTDNS + " "+ STAFE_2_FILE + " "+ STAFE_3_FILE
    print(command)
    os.system(command)

    append_to_file_lines(STAFE_3_FILE, valid_domains)

    command = "python3 " + BIN_MASSDNS + " "+ STAFE_3_FILE + " "+ STAFE_4_FILE
    print(command)
    os.system(command)

    # Store
    valid_domains = readafile(STAFE_5_FILE) + readafile(STAFE_4_FILE)
    valid_domains = list(dict.fromkeys(valid_domains))
    append_to_file_lines(COLLECTED_DNS_SUBDOMAINS, valid_domains)

    tested_domains = readafile(STAFE_0_FILE)
    print("Tested: ")
    print(tested_domains)

    clean()
    
    return 0

def clean_and_sort_list():
    pass

def main():
    PER_TRY = 1
    #lines_ALL_URLs = readafile(ALL_URLs_FILE_TEST)

    lines_ALL_URLs = readafile(ALL_URLs_FILE)
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))

    lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
    lines_VISITED_URLs = list(dict.fromkeys(lines_VISITED_URLs))

    blocklist_URLs = readafile(SE2019_BLOCKLIST)
    blocklist_URLs = list(dict.fromkeys(blocklist_URLs))

    lines_ALL_URLs_new = []

    for url in lines_ALL_URLs:
        url = url.strip(' ')
        if url not in lines_VISITED_URLs:
            if url.startswith( 'www.' ):
                url = url[4:]
                if url not in lines_VISITED_URLs:
                    lines_ALL_URLs_new.append(url)
                continue
            lines_ALL_URLs_new.append(url)

    for url in lines_ALL_URLs_new:
        for blocked_url in blocklist_URLs:
            if blocked_url in url:
                lines_ALL_URLs_new.remove(url)
                break

    if len(lines_ALL_URLs_new) <= 0:
        print("Nothing to work on")


    flag_stop = 0
    while True:
        try:
            tmp_elements = []
            i = 0
            while i < PER_TRY:
                if len(lines_ALL_URLs_new) <= 0:
                    flag_stop = 1
                    break
                    
                tmp_element = lines_ALL_URLs_new.pop(0)
                #print(tmp_element)
                if tmp_element.startswith( 'www.' ):
                    tmp_element = tmp_element[4:]
                if tmp_element not in lines_VISITED_URLs:
                    tmp_elements.append(tmp_element)
                i+=1
            
            
            if len(tmp_elements) <= 0:
                break

            # Set STAFE_0_FILE file
            overwrite_file(STAFE_0_FILE, tmp_elements)
            
            # Do what u need to do
            work()

            # Done
            for tmp_element in tmp_elements:
                append_to_file(VISITED_URLs_FILE, tmp_element)

            print(flag_stop)
            if flag_stop:
                break
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    print(str(PWD)+"/main.py started")
    clean()
    main()
