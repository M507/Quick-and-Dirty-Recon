import sys
ROOT_DIR = "/root/vsvm/"
sys.path.insert(1, ROOT_DIR)

from common import * 
from subcommon import * 

PWD = ROOT_DIR + "/HiddenGems"

PWD_BBTz = ROOT_DIR + "/BBTz"
BBTZ_Storage = PWD_BBTz + "/Storage/"

PWD_LINKFINDERRUNNER = ROOT_DIR + "/LinkFinderRunner" 
LINKFINDERRUNNER_Storage = PWD_LINKFINDERRUNNER + "/Storage/"

PWD_SECRETFINDERRUNNER = ROOT_DIR + "/SecretFinderRunner"
SECRETFINDERRUNNER_Storage = PWD_SECRETFINDERRUNNER + "/Storage/"

PWD_GOBUSTER = ROOT_DIR + "/gobuster" 
GOBUSTER_Storage = PWD_GOBUSTER + "/Storage/"

PWD_GOSPIDER = ROOT_DIR + "/gospider"    
GOSPIDER_Storage = PWD_GOSPIDER + "/Storage/"


for Storage in [BBTZ_Storage,LINKFINDERRUNNER_Storage, SECRETFINDERRUNNER_Storage, GOBUSTER_Storage, GOSPIDER_Storage]:
    command = "rm -rf "+Storage
    print(command)
    os.system(command)

command = "rm -rf /tmp/*"
print(command)
os.system(command)

print("Done : )")