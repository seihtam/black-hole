#!/usr/bin/env python2
import os
from app import create_app, socketio
from werkzeug import SharedDataMiddleware

if __name__ == '__main__':
    app = create_app('sqlite:///app.db', debug=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'app/static'),
    })
    socketio.run(app, host='0.0.0.0', port=8080)
