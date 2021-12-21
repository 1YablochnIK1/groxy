from configparser import ConfigParser
import threading, requests, random, string, sys, os

from colorama import Fore, init

import datetime
from time import sleep
import platform

try:
    if platform.system() == 'Windows':
        os.system('cls')
        os.system('title [Groxy] by 1YablochniK1 ^| V1.0 ^| ~ Loading ~')
        os.system('mode CON COLS=65 LINES=30')
    else:
        os.system('clear')
except:
    pass

valid = 0
invalid = 0
retries = 0
proxies = []
proxies_s5 = []
proxies_https = []
proxy_s5_num = 0
proxy_num = 0
proxy_https_num = 0
lock = threading.Lock()

headers = {'Upgrade-Insecure-Requests':'1', 
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
cfg_path = 'config.ini'

def yellow():
    return '\u001b[33;1m'

def blue():
    return '\u001b[34;1m'

def magenta():
    return '\u001b[35;1m'

def cyan():
    return '\u001b[36;1m'

def red():
    return '\x1b[31;1m'

def green():
    return '\x1b[32;1m'

def reset():
    return '\x1b[0m'

def configW():
    config = ConfigParser()
    parser.read(cfg_path)

    config["Groxy"] = {
        "thread_count": thc,
        "ping_server": pser
    }
    with open(cfg_path, "w") as (f):
        config.write(f)

def configC():
    config = ConfigParser()
    config['Groxy'] = {
     'thread_count':'300',
     "ping_server": "https://google.com"
     }
    with open(cfg_path, 'w') as (f):
        config.write(f)
    configR()


def configR():
    global thc
    global pser
    try:
        parser = ConfigParser()
        parser.read(cfg_path)

        pser = parser.get("Groxy", "ping_server")
        
        try:
            thc = int(parser.get('Groxy', 'thread_count'))
            if thc > 1000:
                thc = 1000
            else:
                if thc == 1000:
                    thc = 1000
        except:
            configC()
        
    except:
        configC()
        configR()

def grab_proxies():
    while True:
        all_proxies = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&country=all&ssl=all&anonymity=all').text
        for proxy in all_proxies.splitlines():
            proxies.append(proxy)

        sleep(600)
        proxies.clear()

def grab_proxies_s5():
    while True:
        all_proxies_s5 = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=5000&country=all&anonymity=all").text
        for proxy_s5 in all_proxies_s5.splitlines():
            proxies_s5.append(proxy_s5)

        sleep(600)
        proxies_s5.clear()

def grab_proxies_https():
    while True:
        all_proxies_https = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&country=all&ssl=yes&anonymity=all').text
        for proxy_https in all_proxies_https.splitlines():
            proxies_https.append(proxy_https)

        sleep(600)
        proxies_https.clear()

def cpm():
    global invalid
    global valid
    old = valid + invalid
    sleep(1)
    new = valid + invalid
    return (new - old) * 60

def main(proxy, proxy_s5, proxy_https):
    global invalid
    global retries
    global valid

    try:
        check = requests.get(pser, headers=headers, proxies={'https': 'http://%s' % proxy}, timeout=3)
        ff = open("https_proxy.txt", "a")
        ff.write(f"{proxy}\n")
        ff.close()
        
        lock.acquire()
        now = datetime.datetime.now()
        nowtime =  str(f"{now.hour}:{now.minute}:{now.second}")
        sys.stdout.write(f'[{cyan()}{nowtime}{reset()}]=[{green()}+++{reset()}] {cyan()}https://{proxy}{reset()}\n')
        lock.release()
        valid += 1
        retries += 1
    except: 
        retries += 1
        invalid += 1

    try:
        check = requests.get(pser, headers=headers, proxies={'http': 'http://%s' % proxy}, timeout=3)
        ff = open("http_proxy.txt", "a")
        ff.write(f"{proxy}\n")
        ff.close()
        
        lock.acquire()
        now = datetime.datetime.now()
        nowtime =  str(f"{now.hour}:{now.minute}:{now.second}")
        sys.stdout.write(f'[{blue()}{nowtime}{reset()}]=[{green()}+++{reset()}] {cyan()}https://{proxy}{reset()}\n')
        lock.release()
        valid += 1
        retries += 1
    except:
        retries += 1
        invalid += 1
    
    try:
        check = requests.get(pser, headers=headers, proxies={"socks5": "socks://%s" % proxy_s5}, timeout=3)
        ff = open("socks5_proxy.txt", "a")
        ff.write(f"{proxy}\n")
        ff.close()

        lock.acquire()
        now = datetime.datetime.now()
        nowtime =  str(f"{now.hour}:{now.minute}:{now.second}")
        sys.stdout.write(f"[{magenta()}{nowtime}{reset()}]=[{green()}+++{reset()}] {cyan()}socks5://{proxy}{reset()}\n")
        lock.release()
        valid += 1
        retries += 2
    except:
        retries += 1
        invalid += 1

configR()

try:
    if platform.system() == 'Windows':
        os.system('cls')
        os.system(f'title [Groxy] by 1YablochniK1 ^| V1.0 ^| ~ {thc} ~')
        os.system('mode CON COLS=65 LINES=30')
except:
    pass

threading.Thread(target=grab_proxies).start()
threading.Thread(target=grab_proxies_s5).start()
threading.Thread(target=grab_proxies_https).start()
threading.Thread(target=cpm).start()
sleep(3)
while threading.active_count() <= thc:
    try:
        threading.Thread(target=main, args=(proxies[proxy_num], proxies_s5[proxy_s5_num], proxies_https[proxy_https_num],)).start()
        proxy_num += 1
        proxy_s5_num += 1
        proxy_https_num += 1
        if proxy_num >= len(proxies):
            proxy_num = 0
        if proxy_s5_num >= len(proxies_s5):
            proxy_s5_num = 0
        if proxy_https_num >= len(proxies_https):
            proxy_https_num = 0
    except:
        lock.acquire()
        now = datetime.datetime.now()
        nowtime =  str(f"{now.hour}:{now.minute}:{now.second}")
        sys.stdout.write(f'[{reset()}{nowtime}{reset()}] [{red()}ERROR{reset()}] {cyan()}Start threads error{reset()}\n')
        lock.release()