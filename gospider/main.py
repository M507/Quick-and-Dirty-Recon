import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 


PWD = ROOT_DIR + "/gospider"
BIN = "/bin/gospider"
XURLS_BIN = "/bin/xurls"
DEPTH = 8

debug = 1

def work(IN_FILE, TMP_URLs_DIR):
    # gospider -S urls.txt -d 8 -o gospider-output.txt
    command = BIN + " -S "+IN_FILE+" -d "+str(DEPTH)+" -o "+TMP_URLs_DIR
    os.system(command)

    return 0

def parse_urls(TMP_URLs_FILE, DOMAIN, TMP_TMP_GOSPIDER):
    command = "cat "+TMP_URLs_FILE+" | "+XURLS_BIN+" | grep "+DOMAIN+" | sed 's/ *$//g' | uniq -u > "+TMP_TMP_GOSPIDER
    print(command)
    os.system(command)
    lines_ALL_URLs = readafile(TMP_TMP_GOSPIDER)
    for i in range(len(lines_ALL_URLs)):
        element = lines_ALL_URLs[i]
        if element[-1] == "/":
            lines_ALL_URLs[i]=lines_ALL_URLs[i][:-1]
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
    # Store
    overwrite_file(FOUND_URLs_FILE,lines_ALL_URLs)
    # Store js files
    lines_ALL_URLs = [url for url in lines_ALL_URLs if url.endswith('.js')]
    overwrite_file(FOUND_JSs_FILE,lines_ALL_URLs)
    
    os.system("rm "+TMP_TMP_GOSPIDER)

def arg_main(URL, IN_FILE, TMP_URLs_DIR, TMP_URLs_FILE, DOMAIN, TMP_TMP_GOSPIDER):
    work(IN_FILE, TMP_URLs_DIR)
    parse_urls(TMP_URLs_FILE, DOMAIN,TMP_TMP_GOSPIDER)

if __name__ == "__main__":
    # python3 main.py <url> /root/vsvm/gospider/Storage/test_urls.txt dwedwer234rded
    print("subzy/main.py started")
    if len(sys.argv)  > 2:
        URL    = sys.argv[1]
        IN_FILE    = sys.argv[2]
        RANDOM = sys.argv[3]
        try:
            os.mkdir( PWD + "/Storage/"+RANDOM)
        except:
            pass
        VISITED_URLs_FILE   = PWD + "/Storage/"+RANDOM+"/visited_urls.txt"
        FOUND_URLs_FILE     = PWD + "/Storage/"+RANDOM+"/found_urls.txt"
        FOUND_JSs_FILE      = PWD + "/Storage/"+RANDOM+"/found_js.txt"
        TMP_URLs_DIR        = PWD + "/Storage/"+RANDOM+"/tmp"
        TMP_TMP_GOSPIDER = "/tmp/"+RANDOM+"_tmp"
        DOMAIN = extract_tld_string(URL)
        TMP_URLs_FILE       = TMP_URLs_DIR + "/" + DOMAIN.replace('.','_')
        for file_name in [VISITED_URLs_FILE,FOUND_URLs_FILE]:
            try:
                open(file_name, mode='w').close()
            except OSError:
                print('Failed creating the file')
            else:
                print(file_name+' File created')
        arg_main(URL, IN_FILE, TMP_URLs_DIR, TMP_URLs_FILE, DOMAIN, TMP_TMP_GOSPIDER)
    else:
        print("no args")
