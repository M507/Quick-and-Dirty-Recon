"""
Tags: OTG-CONFIG-004

Find backups

Usage:
python3 main.py list_of_urls.txt RANDOME_string


In the back end, it should run:
ffuf -u https://example.com/FUZZ -w ./raft-medium-words.txt -s -e .backup,.bck,.bk,.old,.save,.bak,.sav,~,.copy,.orig,.tmp,.txt,.back..swp,.rej,.inc,.src | tee backups-urls.txt


A good word list to use:
https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/raft-medium-words.txt

"""