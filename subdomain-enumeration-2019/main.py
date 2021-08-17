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

def work():

    BIN_MASSDNS = ROOT_DIR + "/massdns"                     + "/main.py"
    BIN_AMASS   = ROOT_DIR + "/Amass"                       + "/main.py"
    BIN_commonspeak2  = ROOT_DIR + "/commonspeak2-wordlists"      + "/main.py"
    BIN_ALTDNS  = ROOT_DIR + "/altdns"                      + "/main.py"


    command = "python3 " + BIN_AMASS + " "+ STAFE_0_FILE + " "+ STAFE_1_FILE
    print(command)
    os.system(command)


    command = "python3 " + BIN_commonspeak2 + " "+ STAFE_0_FILE + " "+ STAFE_1_FILE
    print(command)
    os.system(command)


    command = "python3 " + BIN_MASSDNS + " "+ STAFE_1_FILE + " "+ STAFE_2_FILE
    print(command)
    os.system(command)


    command = "python3 " + BIN_ALTDNS + " "+ STAFE_2_FILE + " "+ STAFE_3_FILE
    print(command)
    os.system(command)

    valid_domains = readafile(STAFE_2_FILE)
    append_to_file_lines(STAFE_3_FILE, valid_domains)

    command = "python3 " + BIN_MASSDNS + " "+ STAFE_3_FILE + " "+ STAFE_4_FILE
    print(command)
    os.system(command)

    # Store
    valid_domains = readafile(STAFE_4_FILE)
    append_to_file_lines(COLLECTED_DNS_SUBDOMAINS, valid_domains)

    tested_domains = readafile(STAFE_0_FILE)
    print("Tested: ")
    print(tested_domains)


    # Clean
    command = "rm "+SE2019_STORAGE+ "/stage* "
    os.system(command)

    command = "cd "+SE2019_STORAGE+ "; touch stage2.txt stage3.txt stage4.txt stage1.txt stage0.txt"
    os.system(command)

    
    return 0

def main():
    #lines_ALL_URLs = readafile(ALL_URLs_FILE_TEST)
    lines_ALL_URLs = readafile(ALL_URLs_FILE)
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
    lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
    lines_ALL_URLs_new = [ url for url in lines_ALL_URLs if url not in lines_VISITED_URLs]
    
    flag_stop = 0
    while True:
        try:
            tmp_elements = []
            i = 0
            while i < 6:
                if len(lines_ALL_URLs_new) <= 0:
                    flag_stop = 1
                    break
                    
                tmp_element = lines_ALL_URLs_new.pop(0)
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
    main()
