import requests as r
import logging 
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ContextManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.s.close()
        if exc_type or exc_value:
            logger.error(exc_type)
            return False
        return True


class HttpConn(ContextManager):
    def __init__(self, config):
        self.config = config
        self.s = r.Session()
        self.s.trust_env = False


class GetConnSession(HttpConn):
    def __enter__(self):
        return self.s.get(
            self.config['URL'],
            params=self.config['PARAMS'],
            verify=self.config['VERIFY'],
            cookies=self.config['COOKIES'],
            headers=self.config['HEADERS'],
            allow_redirects=self.config['REDIRECTS']
        ) 


class PostConnSession(HttpConn):
    def __enter__(self):
        return self.s.post(
            self.config['URL'],
            json=self.config['PAYLOAD'],
            data=self.config['DATA'],
            params=self.config['PARAMS'],
            verify=self.config['VERIFY'],
            cookies=self.config['COOKIES'],
            headers=self.config['HEADERS'],
            allow_redirects=self.config['REDIRECTS']
        )