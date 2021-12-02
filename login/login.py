# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
from .hex2b64 import HB64
from .RSAJS import RSAKey
import sys

def logtime(): return time.strftime("%H:%M:%S", time.localtime())

def logging(foo):
    def wrapper(*args, **kwargs):
        print()
        print('[+]'+logtime()+' %s 尝试登录中...'%(args[0].url))
        start = time.time()
        foo(*args, **kwargs)
        end = time.time()
        duration = end - start
        q = ""
        if duration < 2:
            q = "Good"
        elif duration > 2 and duration < 10:
            q = "Normal"
        else:
            q = "Bad"
        print('[+]'+logtime()+' %s 登录成功!'%(args[0].url))
        print('[+]'+logtime()+' %s 登录用时: %ss, 网络质量: %s'%(args[0].url, str(duration)[:4], q))
    return wrapper

class Loginer():

    sessions = requests.Session()
    time = int(time.time())

    def __init__(self, url, user, passwd):
        self.url = str(url)
        self.user = str(user)
        self.passwd = str(passwd)

    def reflush_time(self):
        self.time = int(time.time())

    def get_public(self):
        
        url = '%s/jwglxt/xtgl/login_getPublicKey.html?time='%(self.url) + \
            str(self.time)
        r = self.sessions.get(url)
        self.pub = r.json()

    def get_csrftoken(self):
        url = '%s/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t='%(self.url) + \
            str(self.time)
        r = self.sessions.get(url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        self.token = soup.find(
            'input', attrs={'id': 'csrftoken'}).attrs['value']

    def process_public(self, str):
        self.exponent = HB64().b642hex(self.pub['exponent'])
        self.modulus = HB64().b642hex(self.pub['modulus'])
        rsa = RSAKey()
        rsa.setPublic(self.modulus, self.exponent)
        cry_data = rsa.encrypt(str)
        return HB64().hex2b64(cry_data)

    def post_data(self):
        try:
            url = '%s/jwglxt/xtgl/login_slogin.html'%(self.url)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': '%s/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t='%(self.url)+str(self.time),
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            }
            self.header = header
            data = {
                'csrftoken': self.token,
                'mm': self.process_public(self.passwd),
                'mm': self.process_public(self.passwd),
                'yhm': self.user
            }
            self.req = self.sessions.post(url, headers=header, data=data)
            self.cookie = self.req.request.headers['cookie']
            ppot = r'用户名或密码不正确'
            if re.findall(ppot, self.req.text):
                print('[!]用户名或密码错误,请查验..')
                sys.exit()
        except Exception as e:
            print('[!]登录失败,请检查网络配置或检查账号密码...')
            print(e)
            sys.exit()

    @logging
    def login(self):
        self.get_public()
        self.get_csrftoken()
        self.post_data()
