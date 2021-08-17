import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/massdns"
MASSDNS_LISTS =  PWD + "/lists"
RESOLVERS_LIST = MASSDNS_LISTS + "/resolvers.txt"
SUBDOMAINS_WORDLIST = PWD + "/subdomains/subdomains.txt"
VISITED_URLs_FILE = PWD + "/Storage/visited_domains.txt"
BIN = PWD + "/bin/massdns"

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




def _exec_and_readlines(cmd, domains):
    try:
        
        domains_str = bytes('\n'.join(domains), 'ascii')
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate(input=domains_str)
        stdout_list = str(stdout)[2:-1].split('\\n')
        stdout_list = [ domain for domain in stdout_list if len(domain) > 1]
        #print(stdout_list)
        return(stdout_list)

    except Exception as ex:
        print("_exec_and_readlines(cmd, domains)")
        print(ex)

def get_massdns(domains):
    records = []
    try:
        massdns_cmd = [
            BIN,
            '-s', '15000',
            '-t', 'A',
            '-o', 'S',
            '-r', RESOLVERS_LIST,
            '--flush'
        ]

        records = _exec_and_readlines(massdns_cmd, domains)
    except Exception as ex:
        print("get_massdns(domains)")
        print(ex)
    return records


def work(domains):
    """
    This function gets only the domain namesm it doesn't care about any of their IPs
    """
    records = get_massdns(domains)
    domains = []
    
    # Get only the domain name
    for domain in records:
        try:
            domain = domain.split(' ')[0]
            # Remove the . at the end 
            if domain[-1] == ".":
                domain = domain[:-1]

            domains.append(domain)
        except:
            pass

    domains = list(dict.fromkeys(domains))
    return domains

def run(IN_FILE_NAME,OUT_FILE_NAME):
    try:
        lines_ALL_URLs = readafile(IN_FILE_NAME)
        # Sort and remove duplicates. 
        lines_ALL_URLs = list(dict.fromkeys(lines_ALL_URLs))
        #lines_VISITED_URLs = readafile(VISITED_URLs_FILE)
        # Get only new domains
        #lines_ALL_URLs_new = [ url for url in lines_ALL_URLs if url not in lines_VISITED_URLs]
        domain_names = [ domain_name.strip("\r").strip("\n").strip(" ") for domain_name in lines_ALL_URLs ] 
        
        # Get valid domain names
        domain_names = work(domain_names)

        # Save
        #append_to_file_lines(OUT_FILE_NAME, domain_names)
        domain_names = list(dict.fromkeys(domain_names))
        if (len(domain_names)-1) >= len(lines_ALL_URLs):
            return
        overwrite_file(OUT_FILE_NAME,domain_names)
    except Exception as ex:
        print("run(FILE_NAME)")
        print(ex)

def test():
    run("/root/vsvm/subdomain-enumeration-2019/Storage/stage1.txt","/root/vsvm/subdomain-enumeration-2019/Storage/stage2.txt")

if __name__ == "__main__":
    print("massdns/main.py started")
    #test()
    if len(sys.argv)  > 2:
        IN_FILE_NAME    = sys.argv[1]
        OUT_FILE_NAME   = sys.argv[2]
        run(IN_FILE_NAME,OUT_FILE_NAME)
    else:
        print("no args")

