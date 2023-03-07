
import urllib.request

def get_public_ip():
    siteurl = "https://ifconfig.me/ip"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'}

    req = urllib.request.Request(siteurl, headers=headers)
    response = urllib.request.urlopen(req)
    page_html = response.read().decode()

    return page_html

public_ip = get_public_ip()
print(public_ip)