#!/usr/bin/env python3
import os
from app import create_app
from cherrypy import wsgiserver
from werkzeug import SharedDataMiddleware

if __name__ == '__main__':
    app = create_app('sqlite:///app.db', debug=False)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'app/static'),
    })

    d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), d)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
