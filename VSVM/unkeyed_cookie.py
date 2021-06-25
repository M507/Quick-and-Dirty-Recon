#https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-cookie
import requests
unkeyed_cookie_prohibited_list = ['session']
unkeyed_cookie_tests = ['soundeffects']

def test():
    BASE_URL = 'https://web-security-academy.net/'
    tmp_session = requests.session()
    headers = {}
    headers["User-Agent"] =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36" 
    response = tmp_session.get(BASE_URL, headers = headers)
    try:
        cookies = tmp_session.cookies
        cookies_dict = cookies.get_dict()
    except Exception as e: 
        print(e)
        cookies_dict = {}

    if len(cookies_dict) > 0:
        for test in unkeyed_cookie_tests:
            print(str(cookies_dict))
            for key,value in cookies_dict.items():
                if key not in unkeyed_cookie_prohibited_list:
                    cookies_dict[key] = test
            print(str(cookies_dict))
            tmp_session = requests.session()
            response = tmp_session.get(BASE_URL, headers = headers, cookies = cookies_dict)
            print(response.request.url)
            print(response.request.body)
            print(response.request.headers)
            print(response.text)

def main():
    test()


main()
