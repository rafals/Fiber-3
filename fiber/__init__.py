from fiber.core import Core
from fiber.vendor.lazyprop import lazyprop
from fiber.cookies import Cookies
import yaml

class Fiber(Core):
    def __lshift__(self, content):
        """ self << 'Text response' """
        return self.response.out.write(content)
    
    @lazyprop
    def config(self):
        """ title = self.config['title'] """
        return yaml.load(file('config.yaml', 'r')) # TODO: absolutize file path
    
    @property
    def cookies(self):
        """ self.cookies.set('key', 'val')
            self.cookies.get('key')
            self.cookies.set('key', 'val', expires_days=10)"""
        return Cookies(self)
    