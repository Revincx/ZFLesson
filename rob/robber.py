import threading

from login.login import Loginer
from .rob import Fetcher


class Robber():

    def __init__(self, url,  config):
        self.url = url
        self.config = config

    def start(self):
        self.instance = Loginer(self.url, self.config['username'], self.config['password'])
        self.instance.login()
        for lesson in self.config['lessons']:
            threading.Thread(target=Fetcher(self.instance, lesson, self.config).rob_it).start()
