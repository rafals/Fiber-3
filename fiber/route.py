import re

class Route(object):
    def __init__(self, pattern):
        self.method, path_pattern = self._split_pattern(pattern)
        self.path_regex = self._path_pattern_to_regex(path_pattern)
    
    def match(self, env):
        return True if self._match_method(env) and self._match_path(env) else False
    
    def params(self, env):
        return self._match_path(env).groupdict()
    
    def _match_method(self, env):
        return self.method is None or self.method == env['REQUEST_METHOD']
    
    def _match_path(self, env):
        return re.match(self.path_regex, env['PATH_INFO'], re.I)
    
    @classmethod
    def _split_pattern(cls, pattern):
        elements = str.split(pattern, ' ')
        #raise ValueError(len(elements))
        if len(elements) == 2:
            method, path_pattern = elements
        elif len(elements) == 1:
            method, path_pattern = None, elements.pop()
        else:
            raise ValueError("Bad format of route template: " + pattern)
        return method, path_pattern
    
    @classmethod
    def _path_pattern_to_regex(cls, path_pattern):
        """Przerabia /ple/ple/{id} na regex"""
        pattern = path_pattern
        var_regex = re.compile(r'\{(\w+)(?::([^}]+))?\}', re.VERBOSE)
        regex = ''
        last_pos = 0
        for match in var_regex.finditer(pattern):
          regex += re.escape(pattern[last_pos:match.start()])
          var_name = match.group(1)
          expr = match.group(2) or '[^/]+'
          expr = '(?P<%s>%s)' % (var_name, expr)
          regex += expr
          last_pos = match.end()
        regex += re.escape(pattern[last_pos:])
        regex = '^%s$' % regex
        return regex