import os
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from utils import GetConnSession,PostConnSession

load_dotenv()

logger = logging.getLogger(__name__)


class BookCourt:
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    def __init__(self):
        self._cookies = None
        self._application_cookie = None
        self.csrf_token = None

    def get_token(self):
        config = {
            'URL': 'https://grandeur8.net/account/login',
            'DATA': None,
            'PAYLOAD': None,
            'PARAMS': None,
            'REDIRECTS': True,
            'VERIFY': True,
            'COOKIES': None,
            'HEADERS': None
        }
        with GetConnSession(config) as s:
            self._cookies = s.cookies
            soup = BeautifulSoup(s.text, features='html.parser')
            self.csrf_token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
            


    def login(self):
        config = {
            'URL': 'https://grandeur8.net/account/login',
            'DATA': {
                '__RequestVerificationToken': self.csrf_token,
                'Username': self.EMAIL,
                'Password': self.PASSWORD,
                'RememberMe': False
            },
            'PAYLOAD': None,
            'PARAMS': None,
            'REDIRECTS': True,
            'VERIFY': True,
            'COOKIES': self._cookies,
            'HEADERS': None
        }
        with PostConnSession(config) as s:
            logger.info(s.cookies)
            print(s.url)
            print(s.status_code)
            # self._application_cookie = s.cookies['.AspNet.ApplicationCookie']
            # logger.info(self._application_cookie)
    
    def execute(self):
        self.get_token()
        self.login()

        

