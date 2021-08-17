import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/altdns"
SUBDOMAINS_WORDLIST = PWD + "/subdomains/subdomains.txt"
ALTDNS_WORDS = PWD + "/words.txt"
BIN = "/usr/local/bin/altdns"

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

def run(IN_FILE_NAME,OUT_FILE_NAME):
    try:
        command = BIN + " -i "+IN_FILE_NAME+" -o "+OUT_FILE_NAME+" -w "+ALTDNS_WORDS+" "
        os.system(command)
    except Exception as ex:
        print("run(FILE_NAME)")
        print(ex)

def test():
    run("/root/vsvm/subdomain-enumeration-2019/Storage/stage1.txt","/root/vsvm/subdomain-enumeration-2019/Storage/stage3.txt")

if __name__ == "__main__":
    print("altdns/main.py started")
    #test()
    if len(sys.argv)  > 2:
        IN_FILE_NAME    = sys.argv[1]
        OUT_FILE_NAME   = sys.argv[2]
        run(IN_FILE_NAME,OUT_FILE_NAME)
    else:
        print("no args")
