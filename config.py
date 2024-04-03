

URLS = [ "https://****.link", "https://****.link" ]

class Endpoint(): 
    __cgi = '/cgi-bin/'
    STATS = __cgi + 'stats.cgi'
    REBOOT = __cgi + 'reboot.cgi'
    MAIN = '/'

HEADRS_L = [
    {
        'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding' :'gzip, deflate, br',
        'Accept-Language' :'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Authorization' : '****',
        'Cache-Control' :'max-age=0',
        'If-Modified-Since' :'Fri, 25 Feb 2022 10:08:05 GMT',
        'If-None-Match' :'W/"1929260457"',
        'Upgrade-Insecure-Requests' :'1',
        'User-Agent' :'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 Edg/122.0.0.0'
    },
    {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Authorization': '****',
        'If-Modified-Since': 'Fri, 31 Dec 2021 03:01:55 GMT',
        'If-None-Match': 'W/"778774664"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
]

min_hash = 6000

ADMIN_CHAT_ID = 1111

API_TOKEN = '****'
