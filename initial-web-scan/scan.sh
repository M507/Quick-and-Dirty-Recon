# bash web-enum-scan.sh https://google.com randomstring


root_dir="/root/vsvm/initial-web-scan/"
STORAGE="Storage/"

domain=$1
randomstring=$2


localStorage=$root_dir$STORAGE$randomstring"/"

echo "Creating "$localStorage
mkdir -p $localStorage 2>/dev/null 


function print_red(){
    echo -e "\e[00;31m[+] $1:\e[00m"
}

print_red "whatweb"
#whatweb $domain | tee $localStorage/$(tlde -u $domain -r)_whatweb.txt

print_red "nikto"
#nikto -h $domain | tee $localStorage/$(tlde -u $domain -r)_nikto.txt

print_red "host"
#host -t ns $(tlde -u $domain -s -r -t) | tee $localStorage/$(tlde -u $domain -r)_host.txt

#echo "Now, do this `host -l www.owasp.org ns1.secure.net # ns1.secure.net is the DNS server and www.owasp.org is your target  `"


