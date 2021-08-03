import os, json, requests, subprocess, tldextract
from random import randint
from time import sleep
from dotenv import load_dotenv
load_dotenv()

ROOT_DIR = "/root/vsvm/"
STORAGE_DIR = ROOT_DIR + "/Storage/"
ALL_URLs_FILE = STORAGE_DIR + "/urls.txt" 
ALL_URLs_FILE_WITH_PARAMETERS = STORAGE_DIR + "/urls_with_parameters.txt" 

API_FILE = STORAGE_DIR + "/api.txt" 
SCOPE_FOLDER = ROOT_DIR + "/Scope"
OUT_OF_SCOPE_FILE = SCOPE_FOLDER + "/out_of_scope_urls.txt" 
OUT_OF_SCOPE_WORDS_FILE = SCOPE_FOLDER + "/out_of_scope_words.txt" 
SCOPE_FILE_NAMES = ['BBDomains.list']


# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
WEBHOOK_URL_CLI = os.environ.get('WEBHOOK_URL_CLI')
BURP_PROXY_IP = os.environ.get('BURP_PROXY_IP')



def slack_notify(text, WEBHOOK_URL = WEBHOOK_URL):
    slack_data = {'text': text}

    response = requests.post(
        WEBHOOK_URL, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    return 1

def readafile(filename):
    try:
        with open(filename,"r") as f: x = f.read().splitlines()
        return x
    except:
        return []

def is_line_in_file(line, filename):
    try:
        lines = readafile(filename)
        if line in lines:
            return True
    except:
        return False


def append_to_file(filename, line):
    try:
        file1 = open(filename, "a")  # append mode 
        file1.write(line+"\n") 
        file1.close()
        return 1
    except:
        return 0


def subprocess_execute_command(command, timeout = None):
    """
    Execute command locally
    :param command:
    :return: stdout
    """
    try:
        if len(command) > 0:
            command = command.split(' ')
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if timeout is not None:
                try:
                    process.wait(timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
            return stdout
    except:
        raise ValueError(
            'subprocess_execute_command returned an error \n'
        )


# This gets a list of hostnames
def get_scope():
    # Read file by file
    all_domains = []
    for FILE_NAME in SCOPE_FILE_NAMES:
        new_domains = readafile(SCOPE_FOLDER + "/" + FILE_NAME)
        all_domains = all_domains + new_domains

    only_hostnames = []
    for domain in all_domains:
        tmp_domain = tldextract.extract(domain).domain
        if len(tmp_domain) > 4:
            only_hostnames.append(tmp_domain)
        else:
            only_hostnames.append(domain)

    # remove duplicates
    only_hostnames = list(dict.fromkeys(only_hostnames))
    return only_hostnames


def extract_tld_string(URL):
    extracted = tldextract.extract(URL)
    if len(extracted.subdomain) > 0:
        tldp = "{}.{}.{}".format(extracted.subdomain,extracted.domain, extracted.suffix)
    else:
        tldp = "{}.{}".format(extracted.domain, extracted.suffix)
    return tldp