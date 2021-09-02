
```

apt install python-pip python3-pip -y
pip install py-altdns
pip3 install -r requirements.txt

wget https://golang.org/dl/go1.17.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.linux-amd64.tar.gz

echo "
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
" >> /etc/profile

go get -u -v github.com/lukasikic/subzy
go install -v github.com/lukasikic/subzy


apt install p7zip-full unzip -y

cd /tmp
wget https://github.com/OJ/gobuster/releases/download/v3.1.0/gobuster-linux-amd64.7z
7z x gobuster-linux-amd64.7z
cd gobuster-linux-amd64/
mv gobuster /bin
chmod +x /bin/gobuster
cd /tmp
wget https://github.com/jaeles-project/gospider/releases/download/v1.1.6/gospider_v1.1.6_linux_x86_64.zip
unzip gospider_v1.1.6_linux_x86_64.zip
cd gospider_v1.1.6_linux_x86_64/
mv gospider /bin


cd LinkFinder
pip3 install -r requirements.txt
python3 setup.py install


mkdir -p /usr/share/wordlists/dirbuster/
cd /usr/share/wordlists/dirbuster/
wget https://github.com/daviddias/node-dirbuster/raw/master/lists/directory-list-2.3-medium.txt


cd /tmp
wget https://github.com/mvdan/xurls/releases/download/v2.3.0/xurls_v2.3.0_linux_amd64
chmod +x xurls_v2.3.0_linux_amd64
mv xurls_v2.3.0_linux_amd64 /bin/xurls

```

