import yaml
import threading
from rob.robber import Robber

print('')
print(" _                                             ")
print("|_)   _   |_     |    _    _   _   _   ._    _ ")
print("| \  (_)  |_)    |_  (/_  _>  _>  (_)  | |  _> ")
print('')
print('')
print('[+]Made By EddieIvan, Modified by Revincx')
print('[+]Github: http://github.com/eddieivan01')
print('')


try:
    config = yaml.load(open('config.yml', 'rb'), Loader=yaml.BaseLoader)
except FileNotFoundError:
    print('[!]配置文件不存在！')
    print('[!]请将config.example.yml重命名为config.yml并正确填写相关配置！')
    exit()

if config['urls'] is None or len(config['urls']) == 0:
    print('[!]请正确填写教务系统的网址!')
    exit()

if config['lessons'] is None or len(config['lessons']) == 0:
    print('[!]请正确填写要选课程的课程号！')
    exit()

for url in config['urls']:
    robber = Robber(url, config)
    threading.Thread(target=robber.start).start()
