
"""
python3 /root/vsvm/HiddenGems/main.py https://gggggogle.com RANDOMESTRING
"""

import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 


PWD = ROOT_DIR + "/HiddenGems"
#BIN =PWD + "/SecretFinder.py"

debug = 1

def fix_double_urls_helper(URL_element, u_string):
    URL_element_list = URL_element.split(u_string)
    tmp_list = []
    for tmp_element in URL_element_list:
        if len(tmp_element) > 1:
            tmp_list.append(u_string+tmp_element)
    return tmp_list

def fix_double_urls(LIST_OF_URLs):
    for i in range(len(LIST_OF_URLs)):
        URL_element = LIST_OF_URLs[i]
        for u_strings in ['http://','https://']:
            if URL_element.count(u_strings) > 1:
                new_elements = fix_double_urls_helper(URL_element, u_strings)
                LIST_OF_URLs.remove(URL_element)
                LIST_OF_URLs = LIST_OF_URLs + new_elements
                continue
    return LIST_OF_URLs

def remove_unwanted_urls(LIST_OF_URLs,BLOCK_LIST):
    tmp_list = []
    for url_tmp in LIST_OF_URLs:
        good_to_go = 1
        for bad_word in BLOCK_LIST:
            if bad_word in url_tmp:
                good_to_go = 0
        if good_to_go:
            tmp_list.append(url_tmp)
    return tmp_list


def work(URL, RANDOM, FOUND_SECRETS_FILE, FOUND_URLs_FILE, TMP_FILE, FOUND_JSs_FILE, BLOCK_LIST_FILE):
    
    BLOCK_LIST = readafile(BLOCK_LIST_FILE)
    BLOCK_LIST = list(dict.fromkeys(BLOCK_LIST))
    
    PWD_BBTz = ROOT_DIR + "/BBTz"
    BIN_BBTz = PWD_BBTz + "/main.py"
    BBTZ_FOUND_JSs_FILE = PWD_BBTz + "/Storage/"+RANDOM+"/found_js.txt"

    PWD_LINKFINDERRUNNER = ROOT_DIR + "/LinkFinderRunner" 
    BIN_LINKFINDERRUNNER = PWD_LINKFINDERRUNNER + "/main.py"
    LINKFINDERRUNNER_FOUND_URLs_FILE = PWD_LINKFINDERRUNNER + "/Storage/"+RANDOM+"/found_urls.txt"

    PWD_SECRETFINDERRUNNER = ROOT_DIR + "/SecretFinderRunner"
    BIN_SECRETFINDERRUNNER  = PWD_SECRETFINDERRUNNER + "/main.py"
    SECRETFINDERRUNNER_FOUND_SECRETS_FILE  = PWD_SECRETFINDERRUNNER + "/Storage/"+RANDOM+"/found_secrets.txt"

    PWD_GOBUSTER = ROOT_DIR + "/gobuster" 
    BIN_GOBUSTER = PWD_GOBUSTER + "/main.py"
    GOBUSTER_FOUND_URLs_FILE = PWD_GOBUSTER + "/Storage/"+RANDOM+"/found_urls.txt"

    PWD_GOSPIDER = ROOT_DIR + "/gospider"    
    BIN_GOSPIDER = PWD_GOSPIDER + "/main.py"
    GOSPIDER_FOUND_JSs_FILE = PWD_GOSPIDER + "/Storage/"+RANDOM+"/found_js.txt"
    GOSPIDER_FOUND_URLs_FILE = PWD_GOSPIDER + "/Storage/"+RANDOM+"/found_urls.txt"


    command = "python3 " + BIN_GOBUSTER + " "+ URL + " "+ RANDOM
    print("HiddenGems: "+command)
    os.system(command)

    command = "python3 " + BIN_GOSPIDER + " "+ URL + " "+ GOBUSTER_FOUND_URLs_FILE + " "+ RANDOM
    print("HiddenGems: "+command)
    os.system(command)

    # Collect all found URLs. 
    print("HiddenGems: "+"Collecting gobuster and gospider results. ")
    GOBUSTER_lines = readafile(GOBUSTER_FOUND_URLs_FILE)
    GOBUSTER_lines = list(dict.fromkeys(GOBUSTER_lines))

    GOSPIDER_lines = readafile(GOSPIDER_FOUND_URLs_FILE)
    GOSPIDER_lines = list(dict.fromkeys(GOSPIDER_lines))

    GOBUSTER_lines_and_GOSPIDER_lines = GOBUSTER_lines + GOSPIDER_lines
    GOBUSTER_lines_and_GOSPIDER_lines = list(dict.fromkeys(GOBUSTER_lines_and_GOSPIDER_lines))

    GOSPIDER_lines.clear()
    GOBUSTER_lines.clear()


    #print("HiddenGems: Overwriting tmp")
    overwrite_file(TMP_FILE,GOBUSTER_lines_and_GOSPIDER_lines)
    
    print("HiddenGems: Starting LinkFinderRunner")
    try:
        # python3 main.py filepath_of_a_file_that_has_js_urls 34nj4io32r
        command = "python3 " + BIN_LINKFINDERRUNNER + " "+ TMP_FILE+ " "+ RANDOM
        print("HiddenGems: "+command)
        os.system(command)
    except Exception as e: 
        print(e)
        print("HiddenGems: "+"ERROR at work() 198234 ")
    
    
    LINKFINDERRUNNER_lines = readafile(LINKFINDERRUNNER_FOUND_URLs_FILE)
    LINKFINDERRUNNER_lines = list(dict.fromkeys(LINKFINDERRUNNER_lines))
    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines = GOBUSTER_lines_and_GOSPIDER_lines + LINKFINDERRUNNER_lines
    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines = list(dict.fromkeys(GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines))

    GOBUSTER_lines_and_GOSPIDER_lines.clear()
    LINKFINDERRUNNER_lines.clear()


    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines = fix_double_urls(GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines)
    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines = list(dict.fromkeys(GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines))
    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines = remove_unwanted_urls(GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines,BLOCK_LIST)

    # Remove zip files and other unwanted URLs     
    tmp_remove_unwanted_extensions = []
    unwanted_extensions = readafile(UNWANTED_EXTENSIONS_FILE)
    unwanted_extensions = list(dict.fromkeys(unwanted_extensions))

    for url_tmp in GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines:
        flag_dont_add = 0
        for unwanted_extension in unwanted_extensions:
            if url_tmp.endswith(unwanted_extension):
                flag_dont_add = 1
        if flag_dont_add == 0:
            tmp_remove_unwanted_extensions.append(url_tmp)
        
    # Store tmp so it can be used next
    overwrite_file(TMP_FILE,tmp_remove_unwanted_extensions)
    tmp_remove_unwanted_extensions.clear()

    # Start getsrc
    try:
        # python3 main.py filepath_of_a_file_that_has_js_urls 34nj4io32r
        command = "python3 " + BIN_BBTz + " "+ TMP_FILE + " "+ RANDOM
        print("HiddenGems: "+command)
        os.system(command)
    except:
        print("HiddenGems: "+"ERROR at work() 234233423")
    
    BBTZ_lines = readafile(BBTZ_FOUND_JSs_FILE)
    BBTZ_lines = list(dict.fromkeys(BBTZ_lines))

    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_only_js = \
    [url_tmp for url_tmp in GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines if url_tmp.endswith('.js')]
    ALL_FOUND_JS_URLS = GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_only_js + BBTZ_lines
    ALL_FOUND_JS_URLS = list(dict.fromkeys(ALL_FOUND_JS_URLS))
    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_and_BBTZ_lines = GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines + BBTZ_lines
    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_and_BBTZ_lines = \
    list(dict.fromkeys(GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_and_BBTZ_lines))

    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines.clear()
    GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_only_js.clear()
    BBTZ_lines.clear()

    print("HiddenGems: Storing the final collections")
    # Store the final collection
    overwrite_file(FOUND_URLs_FILE,GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_and_BBTZ_lines)
    overwrite_file(FOUND_JSs_FILE,ALL_FOUND_JS_URLS)

    ALL_FOUND_JS_URLS = remove_unwanted_urls(ALL_FOUND_JS_URLS,BLOCK_LIST)

    overwrite_file(TMP_FILE,ALL_FOUND_JS_URLS)

    print("HiddenGems: Finding secrets")
    try:
        # python3 main.py filepath_of_a_file_that_has_js_urls 34nj4io32r
        command = "python3 " + BIN_SECRETFINDERRUNNER + " "+ TMP_FILE + " "+ RANDOM
        print("HiddenGems: "+command)
        os.system(command)
    except:
        print("HiddenGems: "+"ERROR at work() 234233423")
 

    ALL_FOUND_JS_URLS = GOBUSTER_lines_and_GOSPIDER_lines_and_LINKFINDERRUNNER_lines_only_js + BBTZ_lines
    ALL_FOUND_JS_URLS = list(dict.fromkeys(ALL_FOUND_JS_URLS))

    SECRETFINDERRUNNER_lines = readafile(SECRETFINDERRUNNER_FOUND_SECRETS_FILE)
    print("HiddenGems: Storing found secrets")
    # Store the final collection
    overwrite_file(FOUND_SECRETS_FILE,SECRETFINDERRUNNER_lines)

    print("HiddenGems: DONE!")


def arg_main(URL, RANDOM, FOUND_SECRETS_FILE, FOUND_URLs_FILE, TMP_FILE, FOUND_JSs_FILE, BLOCK_LIST_FILE):

    try:
        work(URL, RANDOM, FOUND_SECRETS_FILE, FOUND_URLs_FILE, TMP_FILE, FOUND_JSs_FILE, BLOCK_LIST_FILE)
    except:
        print("HiddenGems/main.py arg_main Error 412341235")
    
    return 0

if __name__ == "__main__":
    # python3 main.py URL.com 34nj4io32r
    WHOAMI = "HiddenGems/main.py"
    SCOPE = PWD + "/Scope/"
    print(WHOAMI + " started")
    if len(sys.argv)  > 2:
        URL     = sys.argv[1]
        RANDOM      = sys.argv[2]
        try:
            try:
                os.mkdir( PWD + "/Storage/")
            except:
                print(WHOAMI + " Error 1")
            try:
                os.mkdir( PWD + "/Storage/"+RANDOM+"/")
            except:
                print(WHOAMI + " Error 2")
            try:
                os.mkdir(SCOPE)
            except:
                print(WHOAMI + " Error 3")
        except:
            pass
        FOUND_SECRETS_FILE  = PWD + "/Storage/"+RANDOM+"/found_secrets.txt"
        FOUND_URLs_FILE     = PWD + "/Storage/"+RANDOM+"/found_urls.txt"
        FOUND_JSs_FILE      = PWD + "/Storage/"+RANDOM+"/found_Javascripts.txt"
        TMP_FILE            = "/tmp/"+RANDOM+"_HiddenGems.txt"
        BLOCK_LIST_FILE             = SCOPE + "Blocked_words.txt"
        UNWANTED_EXTENSIONS_FILE    = SCOPE + "Unwanted_Extensions.txt"
        for file_name in [FOUND_SECRETS_FILE,FOUND_URLs_FILE,TMP_FILE, FOUND_JSs_FILE]:
            try:
                open(file_name, mode='w').close()
            except OSError:
                print('Failed creating the file')
            else:
                print(file_name+' File created')
        arg_main(URL, RANDOM, FOUND_SECRETS_FILE, FOUND_URLs_FILE, TMP_FILE, FOUND_JSs_FILE, BLOCK_LIST_FILE)
    else:
        print("no args")
