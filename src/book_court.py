import os
import logging
import requests
import datetime
import json
import asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from utils import GetConnSession, PostConnSession, exponential_backoff

load_dotenv()

logger = logging.getLogger(__name__)


class BookCourt:
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    def __init__(self):
        self.jar = requests.cookies.RequestsCookieJar()
        self._csrf_token = None

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
        with GetConnSession(config) as r:
            if r.status_code >= 400:
                logger.error(r.text)
                raise Exception('unable to get token')
            self.jar.update(r.cookies)
            soup = BeautifulSoup(r.text, features='html.parser')
            self._csrf_token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
            logger.info('retrieve token successful')
            
    def login(self):
        config = {
            'URL': 'https://grandeur8.net/account/login',
            'DATA': {
                '__RequestVerificationToken': self._csrf_token,
                'Username': self.EMAIL,
                'Password': self.PASSWORD,
                'RememberMe': False
            },
            'PAYLOAD': None,
            'PARAMS': None,
            'REDIRECTS': False,
            'VERIFY': True,
            'COOKIES': self.jar,
            'HEADERS': None
        }
        with PostConnSession(config) as r:
            if r.status_code >= 400:
                logger.error(r.text)
                raise Exception('unable to login')
            self.jar.update(r.cookies)
            logger.info('login successful')
    
    async def get_login_session(self):
        # execute at 23:59:00
        await asyncio.sleep(1)
        logger.info('attempting to login...')
        self.get_token()
        self.login()
        
    
    async def prepare_book_court(self):
        # to run 3s before 00:00:00
        # assumes login cookie has been secured for faster request
        # to send multiple requests to server for higher chance of booking
        # similar to DDoS

        next_week_date = datetime.date.today() + datetime.timedelta(days=7)
        book_date = f'{next_week_date.strftime("%Y-%m-%d")}T11:00:00.000Z'  # 2022-09-19T06%3A00%3A00.000Z
        
        await asyncio.sleep(57)
        logger.info('attempting to book court...')
        
        config = {
            'URL': 'https://grandeur8.net/facilities/booking',
            'DATA': {
                'FacilityId': 92,
                'FacilityTypeId': 1041,
                'BookDate': book_date,
                'BookHours': 1,
                'UnitId': 0,
                'UserId': 0,
                'Peak': False,
                'DropDown1': None,
            },
            'PAYLOAD': None,
            'PARAMS': None,
            'REDIRECTS': False,
            'VERIFY': True,
            'COOKIES': self.jar,
            'HEADERS': {'Content-Type': 'application/x-www-form-urlencoded'},
        }

        self.book_court(config, book_date)

    @exponential_backoff(Exception)
    def book_court(self, config, book_date):
        with PostConnSession(config) as r:
            resp = json.loads(r.text)
            if r.status_code >= 400 or resp['alert']['Heading'] != 'Booking Successful':
                logger.error(r.text)
                raise Exception(f'unable to book court at {book_date}')
            logger.info(f'booking for {book_date} successful')

    async def execute(self):
        # to run both functions concurrently
        # first is to retrieve login session
        # second is to book court with session cookies
        await asyncio.gather(self.get_login_session(), self.prepare_book_court())


    
        
'''
FacilityId: 92
FacilityTypeId: 1041
BookDate: 2022-09-19T04:00:00.000Z  2022-09-19T06%3A00%3A00.000Z  
BookHours: 1
UnitId: 0
UserId: 0
Peak: false
DropDown1: 

Booking for 19Sept Monday, 12-1pm
'''      

'''
{'alert': {'Heading': 'Booking Successful', 'Type': 'success', 'Body': 'Your booking has been reserved. An email confirming your booking has been sent to <strong>patricialim38@hotmail.com</strong>. Please ensure that you have <strong>read the booking rules and paid any necessary fees</strong> before using the facility. You are able to print a receipt of your booking (if required) via the booking list page <a href=/facilities/booking>here</a>', 'Dismissable': False}, 'result': {'Email': 'patricialim38@hotmail.com', 'BookingId': 896819}}
'''