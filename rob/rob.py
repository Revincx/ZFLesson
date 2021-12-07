import threading
import json
import time
import requests
import datetime
import re

from login.login import Loginer
from bs4 import BeautifulSoup
from os import _exit

THREAD_FLAG = True
MAX_PROCESS = 2


def logtime(): return time.strftime("%H:%M:%S", time.localtime())


def current_month(): return datetime.datetime.now().month


class Fetcher():

    def __init__(self, instance: Loginer, lesson_id: str, config):
        self.lesson_id = lesson_id
        self.instance = instance
        self.sessions = instance.sessions
        self.url = instance.url
        self.cookie = instance.cookie
        self.user = config['username']
        self.config = config

        if(config['njdm_id'] is None or len(config['njdm_id']) == 0):
            self.njdm_id = self.user[:4]
            self.bh_id = self.user[2:4] + self.user[4:10]
        else:
            self.njdm_id = config['njdm_id']
            self.bh_id = config['njdm_id'][2:4] + self.user[4:10]

        if(config['zyh_id'] is None or len(config['zyh_id']) == 0):
            self.zyh_id = self.user[4:8]
        else:
            self.zyh_id = config['zyh_id']

        if(config['wait_time'] is None or len(config['wait_time']) == 0):
            self.wait_time = 5
        else:
            self.wait_time = int(config['wait_time'])

        if(config['thread_num'] is None or len(config['thread_num']) == 0):
            self.thread_num = MAX_PROCESS
        else:
            self.thread_num = int(config['thread_num'])

        self.header_1 = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self.url+'/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+self.user,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }

        self.header_2 = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Referer': self.url+'/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+self.user,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Cookie': self.cookie
        }

    def lessons_info(self):

        print('[+]'+logtime()+' 尝试获取课程信息...')
        # try:
        index_url = self.url + \
            '/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+self.user
        search_url = self.url + \
            '/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su='+self.user
        choose_url = self.url + \
            '/jwglxt/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su='+self.user
        rob_url = self.url + \
            '/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su='+self.user
        response = self.sessions.get(index_url, headers=self.header_1)
        if "当前不属于选课阶段" in response.text:
            print('[!]'+logtime()+' 未到选课时间，等待 %d 秒后重试...' % (self.wait_time))
            return -1
            # _exit(-1)
        try:
            xkkz = re.findall("onclick=\"queryCourse\(this,'10','([0-9A-F]{32})','([0-9]{4})','([0-9]{4})'\)\" role=\"tab\" data-toggle=\"tab\">通识选修课",
                              response.text)[0][0]
        except:
            text = BeautifulSoup(response.text, "html.parser")
            xkkz = text.findAll(name='input',
                                attrs={
                                    'type': "hidden",
                                    'name': "firstXkkzId",
                                    'id': "firstXkkzId"
                                })[0].attrs['value']
        data = {
            'bh_id': self.bh_id,
            'bklx_id': '0',
            'ccdm': '3',
            'filter_list[0]': self.lesson_id,
            'jg_id': '0102',
            'jspage': '10',
            'kkbk': '0',
            'kkbkdj': '0',
            'kklxdm': '10',
            'kspage': '1',
            'njdm_id': self.njdm_id,
            # 'njdmzyh':' ',
            'rwlx': '2',
            'sfkcfx': '0',
            'sfkgbcx': '0',
            'sfkknj': '0',
            'sfkkzy': '0',
            'sfkxq': '0',
            'sfrxtgkcxd': '1',
            'sfznkx': '0',
            'tykczgxdcs': '10',
            'xbm': '1',
            'xh_id': self.user,
            'xkly': '0',
            'xkxnm': '2021',
            'xkxqm': '3' if current_month() > 5 and current_month() < 8 else '12',
            'xqh_id': '1',
            'xsbj': '4294967296',
            'xslbdm': '421',
            'zdkxms': '0',
            'zyfx_id': 'wfx',
            'zyh_id': self.zyh_id
        }
        search_result = requests.post(search_url, data=data,
                                      headers=self.header_2).json()
        # 输出搜索结果
        # print(search_result)
        if len(search_result['tmpList']) == 0:
            print('[!]'+ logtime() + ' 没有找到课程 ' + self.lesson_id + ' !')
            _exit(-1)
        kch = search_result['tmpList'][0]['kch_id']
        jxb = search_result['tmpList'][0]['jxb_id']
        kcmc = search_result['tmpList'][0]['kcmc']
        self.kcmc = kcmc
        xf = search_result['tmpList'][0]['xf']

        # 获取do_jxb_id

        preChooseUrl = self.url + \
            '/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=' + self.user

        doJxbReqData = {
            'bh_id': self.bh_id,
            'bklx_id': '0',
            'ccdm': '3',
            'filter_list[0]': self.lesson_id,
            'jg_id': '0102',
            'kkbk': '0',
            'kkbkdj': '0',
            'kklxdm': '10',
            'njdm_id': self.njdm_id,
            'rwlx': '2',
            'sfkcfx': '0',
            'sfkknj': '0',
            'sfkkzy': '0',
            'sfkxq': '0',
            'sfkkjyxdxnxq': '0',
            'sfznkx': '0',
            'xbm': '1',
            'xkly': '0',
            'xkxnm': '2021',
            'xkxqm': '3' if current_month() > 5 and current_month() < 8 else '12',
            'xqh_id': '1',
            'xsbj': '4294967296',
            'xslbdm': '421',
            'zdkxms': '0',
            'zyfx_id': 'wfx',
            'zyh_id': self.zyh_id,
            'rlkz': '0',
            'kch_id': kch,
            'xkkz_id': xkkz,
            'cxbj': '0',
            'fxbj': '0',
            'kzybkxy': '0'
        }

        doJxbResponse = requests.post(
            url=preChooseUrl, data=doJxbReqData, headers=self.header_2)
        # print(doJxbResponse.content)
        doJxbData = json.loads(doJxbResponse.text)
        # print(doJxbData)

        self.rob_data = {
            'cxbj': '0',
            'jxb_ids': doJxbData[0]['do_jxb_id'],
            'kch_id': kch,
            'kcmc': '('+kch+')'+kcmc+' - '+xf+' 学分',
            'kklxdm': '10',
            'njdm_id': self.njdm_id,
            'qz': '0',
            'rlkz': '0',
            'rlzlkz': '1',
            'rwlx': '2',
            'sxbj': '1',
            'xkkz_id': xkkz,
            'xklc': '2',
            'xkxnm': '2021',
            'xkxqm': '3' if current_month() > 5 and current_month() < 8 else '12',
            # 'xsbxfs':'0',
            'xxkbj': '0',
            'zyh_id': self.zyh_id
        }
        print('[+]'+logtime()+' 课程信息获取成功!')
        # except:
        #    print('[+]'+logtime()+' 获取失败，请查验课程代号')
        #   _exit(-1)

    def lessons(self, no):
        global THREAD_FLAG
        url = self.url + \
            '/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=' + self.user
        # DEBUG
        # print('请求信息: ')
        # print(self.rob_data)
        print('[+]'+logtime()+' Thread-'+no+' Start')

        max_try = 6
        current_try = 0
        while True:
            if current_try >= max_try:
                break
            if THREAD_FLAG:
                try:
                    response = requests.post(url, data=self.rob_data,
                                             headers=self.header_2, timeout=5)
                    if len(response.text) > 10000 or response.status_code > 300:
                        with open('relogin.txt', 'a') as logger:
                            logger.write(logtime()+' relogin\n')
                        self.instance.login()
                    print('[*]'+logtime()+' Thread-'+no+'  请求成功')
                    if response.json()['flag'] != '1':
                        #print('[*]'+logtime()+' Thread-'+no+'  异常!')
                        print('[*]'+logtime()+' 异常状态码: ' +
                              response.json()['msg'])
                        raise Exception(response.json()['msg'])
                    print('[*]'+logtime()+' Thread-'+no+'  Success!')
                    print('[*]'+logtime()+' '+self.kcmc+'  抢课成功!')
                    print('[+]'+logtime()+' 程序即将退出...')
                    THREAD_FLAG = False
                    current_try += 1
                except KeyboardInterrupt:
                    _exit(-1)
                except Exception as e:
                    print('[*]'+logtime()+' Thread-'+no+'  Fail')
                    if str(e.args[0]).find('冲突') != -1:
                        print('[+]'+logtime()+' 本线程即将退出...')
                        THREAD_FLAG = False
                    if str(e.args[0]).split(',')[0] == '0':
                        if self.config['retry'] == 'true':
                            print('[!]'+logtime()+' 课程人数已满，正在重试...')
                            THREAD_FLAG = True
                            time.sleep(0.5)
                        else:
                            print('[!]'+logtime()+' 课程人数已满，线程即将退出...')
                            THREAD_FLAG = False
            else:
                print('[+]'+logtime()+' Thread-'+no+' Close')
                return

    def generate_thread(self, count):
        self.thread = []
        for i in range(count):
            self.thread.append(threading.Thread(
                target=self.lessons, args=(str(i+1),)))

    def rob_it(self):
        self.generate_thread(self.thread_num)
        while True:
            if self.lessons_info() == -1:
                time.sleep(self.wait_time)
                continue
            break
        for pro in self.thread:
            pro.start()
