import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/Burp"
VISITED_URLs_FILE = PWD + "/Storage/visited_urls.txt"

debug = 1


# Burp file only 
from urllib.parse import unquote, urlparse, parse_qs
from pathlib import PurePosixPath

# Disable  Unverified HTTPS request is being made.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BURP_PROXY = {"http": "http://"+BURP_PROXY_IP+":8080", "https": "http://"+BURP_PROXY_IP+":8080"}
headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36"}


def work(TARGET):
    try:
        r = requests.get(TARGET, proxies=BURP_PROXY, headers=headers, verify=False, timeout=10)
    except Exception as e: print(e)


def get_path_and_q(URL):
    try:
        path = PurePosixPath(
            unquote(
                urlparse(
                    URL
                ).path
            )
        )
        # .replace(' ','')
        parsed_url = urlparse(URL)
        query = parse_qs(parsed_url.query)
        query = sorted(query.items())
        query_string = str(query).replace(' ','')
        path_string = str(path).replace(' ','')
        return path_string, query_string
    except:
        "",""

def main():
    allowed_strings_slash_domains = get_scope()

    

    lines_ALL_URLs = readafile(ALL_URLs_FILE_WITH_PARAMETERS)
    print("lines_ALL_URLs" + str(lines_ALL_URLs))
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
    print("lines_ALL_URLs" + str(lines_ALL_URLs))
    lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
    print("lines_VISITED_URLs" + str(lines_VISITED_URLs))
    lines_ALL_URLs_new = [ url for url in lines_ALL_URLs if url not in lines_VISITED_URLs]
    print("lines_ALL_URLs_new" + str(lines_ALL_URLs_new))
    
    random_sleep_flag = 0

    for line in lines_ALL_URLs:
        try:
            # In case I am editing the out of scope list.. it update itself without rerunning the script again
            lines_ALL_Out_Of_Scope_URLs = readafile(OUT_OF_SCOPE_FILE)
            lines_ALL_Out_Of_Scope_words = readafile(OUT_OF_SCOPE_WORDS_FILE)

            line = line.strip("\r").strip("\n").strip(" ")
            path_string, query_string = get_path_and_q(line)
            URL_and_PATH = extract_tld_string(line) + path_string
            tobe_stored_url = URL_and_PATH +","+(query_string)
            print(tobe_stored_url)

            # Needs to be refreshed since somehting new has been added
            # Check if it has been visited before
            lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
            if tobe_stored_url in lines_VISITED_URLs:
                continue

            # Your usual website that you don't want to scan
            # Check if this is one of your no no sites
            stop=0
            for out_of_scope_url in lines_ALL_Out_Of_Scope_URLs:
                if URL_and_PATH in out_of_scope_url:
                    MESSAGE = "The word '"+str(URL_and_PATH) + "' is in '"+str(out_of_scope_url)+"'"
                    print(MESSAGE)
                    stop=1
                    break
            if stop:
                continue
            

            # Check if this is a certain type of sites like blogs .. 
            # example if "blog" in the url.. it should stop.
            for out_of_scope_word in lines_ALL_Out_Of_Scope_words:
                if out_of_scope_word in line:
                    MESSAGE = "The word '"+str(out_of_scope_word) + "' is in '"+str(line)+"'"
                    print(MESSAGE)
                    stop=1
                    break
            if stop:
                continue
            
            # If no query just pass ... 
            if "[]" == query_string:
                append_to_file(VISITED_URLs_FILE, tobe_stored_url)
                MESSAGE = "This '"+str(line) + "' has no query_string"
                print(MESSAGE)
                continue
            
            if len(line) > 1:
                random_sleep_flag += 1
                
                # Do what u need to do
                MESSAGE = "Sending to Burp: "+ str(line)
                print(MESSAGE)
                slack_notify(MESSAGE, WEBHOOK_URL_CLI)
                work(line)
                # Done
                append_to_file(VISITED_URLs_FILE, tobe_stored_url)

                # Wait before moving on to the next target.
                sleep(10)

            if (int(random_sleep_flag) >= 10):
                sleep_time = randint(10,100)
                MESSAGE = "Sleeping for "+str(sleep_time) + " seconds" 
                print(MESSAGE)
                sleep(sleep_time)
                random_sleep_flag = 0

        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    print("Burp/burp.py started")
    main()


