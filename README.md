

This is a personal reconnaissance and vulnerability scanning project. This project integrates the following tools.

### Integrated projects
- https://portswigger.net/burp/pro
- https://github.com/OWASP/Amass
- https://github.com/infosec-au/altdns
- https://github.com/blechschmidt/massdns
- https://github.com/hakluke/haktrails
- https://github.com/LukaSikic/subzy
- https://github.com/assetnote/commonspeak2-wordlists
- https://github.com/anshumanpattnaik/http-request-smuggling
- https://github.com/GerbenJavado/LinkFinder
- https://github.com/mvdan/xurls
- https://github.com/jaeles-project/gospider
- https://github.com/m4ll0k/SecretFinder
- https://github.com/OJ/gobuster

### How does it work?
Read the code files, and you will understand it : )

### How to integrate other tools

```txt
For every project do the next:
    A folder with:
        main.py
        Storage/visited_urls.txt
Example is provided
```

Add your slack webhook in `.env` file, an example:
```
WEBHOOK_URL=https://hooks.slack.com/services/AAAAAAAAAAAAAAAAAAAAAAA
```


### Directory tree

![Drag Racing](Img/example.png)