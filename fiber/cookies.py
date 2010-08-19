from fiber.vendor.lilcookies import LilCookies

class Cookies(object):
  def __init__(self, handler):
      self._lilcookies = LilCookies(handler, handler.config['cookie_secret'])
  
  def get(self, key, val=None):
      result = self._lilcookies.get_secure_cookie(key)
      return result or val
  
  def set(self, key, val, expires_days=365, **kwargs):
    return self._lilcookies.set_secure_cookie(key, val, expires_days, **kwargs)
  
  def delete(self, key):
    return self._lilcookies.clear_cookie(key)