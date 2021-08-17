import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/commonspeak2-wordlists"
SUBDOMAINS_WORDLIST = PWD + "/subdomains/subdomains.txt"
VISITED_URLs_FILE = PWD + "/Storage/visited_domains.txt"
#BIN = "/root/amass_linux_amd64/amass"

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

def work(target,OUT_FILE_NAME):
    domains_list = []
    scope = target
    wordlist = open(SUBDOMAINS_WORDLIST).read().split('\n')

    for word in wordlist:
        if not word.strip(): 
            continue
        domain = '{}.{}'.format(word.strip(), scope)
        domains_list.append(domain)

    if append_to_file_lines(OUT_FILE_NAME, domains_list):
        print("append_to_file_lines error work(target)")
        return 1

    return 0

def run(IN_FILE_NAME,OUT_FILE_NAME):
    try:
        lines_ALL_URLs = readafile(IN_FILE_NAME)
        # Sort and remove duplicates. 
        lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
        #lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
        # Get only new domains
        #lines_ALL_URLs_new = [ url for url in lines_ALL_URLs if url not in lines_VISITED_URLs]
        
        for domain_name in lines_ALL_URLs:
            try:
                domain_name = domain_name.strip("\r").strip("\n").strip(" ")
                # Needs to be refreshed since somehting new has been added
                #lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
                #if domain_name in lines_VISITED_URLs:
                #    continue
                #else:
                #    pass
                if len(domain_name) > 1:
                    # Do what u need to do
                    work(domain_name,OUT_FILE_NAME)
                    # Done
                    #append_to_file(VISITED_URLs_FILE, domain_name)
            except Exception as ex:
                print(ex)
    except Exception as ex:
        print("run(FILE_NAME)")
        print(ex)

if __name__ == "__main__":
    print("commonspeak2-wordlists/commonspeak2-wordlists.py started")
    if len(sys.argv)  > 2:
        IN_FILE_NAME    = sys.argv[1]
        OUT_FILE_NAME   = sys.argv[2]
        run(IN_FILE_NAME,OUT_FILE_NAME)
    else:
        print("no args")

