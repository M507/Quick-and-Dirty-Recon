import sys, requests, time
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 


PWD = ROOT_DIR + "/x-forwarded"
VISITED_URLs_FILE = PWD + "/Storage/visited_urls.txt"

debug = 1
WAIT_TIME = 5
KEY_WORD = "soundeffects"

def verify(stdout):
    try:
        if KEY_WORD in stdout:
            return 1
    except Exception as ex:
            print(ex)
    return 0


def send(BASE_URL, headers = None, params = None):
    if headers is not None:
        headers["User-Agent"] =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36" 
    response = requests.get(BASE_URL, headers=headers, params=params)
    return response.text


def work(URL):
    httpheaders = ["X-Forwarded-Host","X-Forwarded-For", "X-Forwarded-Proto"]
    for header in httpheaders:
        headers = {}
        headers[header]= KEY_WORD
        try:
            text = send("https://"+URL, headers = headers)
        except Exception as ex:
            print("work1 "+str(ex))
        try:
            text = send("http://"+URL, headers = headers)
        except Exception as ex:
            print("work2 "+str(ex))
            return 0
        if debug:
            print("Testing: "+str(URL))
        if verify(text):
            message = PWD + "/x-forwarded.py found something! '" + URL + "'" + (str(headers))
            slack_notify(message)
            return 1
        time.sleep(1)
    
    
def test2():
    BASE_URL = "https://cc.web-security-academy.net/"
    headers = {}
    headers["X-Forwarded-Host"]= KEY_WORD
    text = send(BASE_URL, headers = headers)
    

def test1():
    BASE_URL = "https://cc.web-security-academy.net/"
    work(BASE_URL)


def main():
    lines_ALL_URLs = readafile(ALL_URLs_FILE)
    lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
    lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
    lines_ALL_URLs_new = [ url for url in lines_ALL_URLs if url not in lines_VISITED_URLs]
    lines_ALL_URLs = prepare_brute_force_list(lines_ALL_URLs_new)
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
                    if WAIT_TIME > 0:
                        time.sleep(WAIT_TIME)
                    work(line)
                    # Done
                    append_to_file(VISITED_URLs_FILE, line)
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    print("x-forwarded/x-forwarded.py started")
    main()
