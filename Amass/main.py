import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/Amass"
VISITED_URLs_FILE = PWD + "/Storage/visited_domains.txt"
BIN = "/root/amass_linux_amd64/amass"

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
    stdout_list = []
    command = BIN + " enum --passive -d "+ target
    stdout = str(subprocess_execute_command(command))

    stdout_list = str(stdout)[2:-1].split('\\n')
    stdout_list = [ domain for domain in stdout_list if len(domain) > 1]
    if debug:
        print("print(stdout_list)")
        print(stdout_list)

    return stdout_list

def main():
    # For test usage only
    #lines_ALL_URLs = readafile(ALL_URLs_FILE_TEST)

    lines_ALL_URLs = readafile(ALL_URLs_FILE)
    # Sort and remove duplicates. 
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
    lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
    # Get only new domains
    lines_ALL_URLs_new = [ url for url in lines_ALL_URLs if url not in lines_VISITED_URLs]
    
    
    for domain_name in lines_ALL_URLs:
        try:
            domain_name = domain_name.strip("\r").strip("\n").strip(" ")
            # Needs to be refreshed since somehting new has been added
            lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
            if domain_name in lines_VISITED_URLs:
                continue
            else:
                if len(domain_name) > 1:
                    # Do what u need to do
                    work(domain_name)
                    # Done
                    append_to_file(VISITED_URLs_FILE, domain_name)
        except Exception as ex:
            print(ex)


def arg_main(IN_FILE_NAME,OUT_FILE_NAME):
    lines_ALL_URLs = readafile(IN_FILE_NAME)
    # Sort and remove duplicates. 
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
    domain_names = [] 
    for domain_name in lines_ALL_URLs:
        try:
            domain_name = domain_name.strip("\r").strip("\n").strip(" ")
            # Needs to be refreshed since somehting new has been added

            # Do what u need to do
            domain_names_tmp = work(domain_name)
            domain_names = domain_names + domain_names_tmp
        except Exception as ex:
            print(ex)
    domain_names = list(dict.fromkeys(domain_names))
    overwrite_file(OUT_FILE_NAME,domain_names)

def test():
    arg_main("/root/vsvm/subdomain-enumeration-2019/Storage/stage1.txt","/root/vsvm/subdomain-enumeration-2019/Storage/stage2.txt")

if __name__ == "__main__":
    print("Amass/main.py started")
    #main()
    #test()
    if len(sys.argv)  > 2:
        IN_FILE_NAME    = sys.argv[1]
        OUT_FILE_NAME   = sys.argv[2]
        arg_main(IN_FILE_NAME,OUT_FILE_NAME)
    else:
        print("no args")
