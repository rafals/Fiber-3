import os
import webob.exc
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from fiber.route import Route

class Core(object):
    __instances = []
    
    def __init__(self, route):
        self.__route = Route(route)
        
    def __call__(self, action):
        self.__action = action
        self.__instances.append(self)
        return action
    
    @classmethod
    def __wsgi_app(cls, env, start_response):
        for i in cls.__instances:
            if i.__route.match(env):
                i.request, i.response = webapp.Request(env), webapp.Response()
                result = i.__action(i, **i.__route.params(env))
                i.response.wsgi_write(start_response)
                return [result or '']
        return webob.exc.HTTPNotFound('Error 404')(env, start_response)
        
    @classmethod
    def run(cls):
        run_wsgi_app(cls.__wsgi_app)