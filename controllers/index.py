from app import app

@app('/')
def index(self):
    return hello(self, name='Guest')

@app('GET /hello/{name}')
@app('GET /hello')
def hello(self, name='World'):
    return 'Hello, %s!' % name

@app('GET /name')
def name(self, name='gosciu'):
    return """<html>
<body>
    <p>Witaj, %s!</p>
    <form action="/name" method="POST">
        <input type="text" name="name" />
        <input type="submit" value="podaj" />
    </form>
</body>
</html>""" % name

@app('POST /name')
def post_name(self):
    return name(self, name=self.request.get('name', 'gosciu'))

@app('/config')
def config(self):
    return self.config['cookie_secret']

@app('/cookies')
def cookies(self):
    id = self.cookies.get('id') or str(0)
    id2 = str(int(id) + 1)
    self.cookies.set('id', id2)
    return str(id2)
     

if __name__ == '__main__':
    app.run()