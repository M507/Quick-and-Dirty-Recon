import os, json, requests, subprocess
from dotenv import load_dotenv
load_dotenv()

ROOT_DIR = "/root/vsvm/"
STORAGE_DIR = ROOT_DIR + "/Storage/"
ALL_URLs_FILE = STORAGE_DIR + "/urls.txt" 

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

def slack_notify(text):
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

