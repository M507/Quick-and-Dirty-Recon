

apt install python-pip python3-pip -y
pip3 install -r requirements.txt

wget https://golang.org/dl/go1.17.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.linux-amd64.tar.gz

echo "
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
" >> /etc/profile

go get -u -v github.com/lukasikic/subzy
go install -v github.com/lukasikic/subzy
