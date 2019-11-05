# coding: utf-8


__author__ = 'Catarina Silva'
__version__ = '0.1'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import sys
import socket
import pickle
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs


USER_AGENT_LINUX_FIREFOX55 = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'


def send_msg(sock, msg, addr):
    data = pickle.dumps(msg)
    l = len(data)
    sock.sendto(str(l).encode(), addr)
    sock.sendto(data, addr)


def recv_msg(sock):
    l, addr = sock.recvfrom(4)
    l = int(l.decode('utf-8'))
    data, addr = sock.recvfrom(l)
    return pickle.loads(data), addr


def meta_redirect(content):
    soup  = bs(content, features='html.parser')
    result_upper = soup.select_one('meta[HTTP-EQUIV="REFRESH"]')
    result_lower = soup.select_one('meta[http-equiv="refresh"]')
    
    if result_upper:
        wait,text=result_upper["content"].split(";")
        if text.strip().startswith("url="):
            url=text[5:]
            return url
    
    if result_lower:
        wait,text=result_lower["content"].split(";")
        if text.strip().startswith("url="):
            url=text[5:]
            return url
    
    return None
​
​
def fetch_raw_html(url: str, user_agent=USER_AGENT_LINUX_FIREFOX55):
    header = {'User-agent': user_agent}
    reply = requests.get(url, headers = header, verify=False, allow_redirects=True)
​
    if reply.status_code == 200:
        redirect_url = meta_redirect(reply.text)
        if redirect_url:
            return fetch_raw_html(redirect_url, user_agent)
        else:
            return reply.text
    else:
        return None


def fetch_rendered_html(url: str, driver: webdriver):
    driver.get(url)
    html_rendered = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    redirect_url = meta_redirect(html_rendered)
    if redirect_url:
        return fetch_rendered_html(redirect_url, driver)
    else:
        return html_rendered


def progress_bar(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
