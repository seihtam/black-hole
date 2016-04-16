from app import create_app, socketio
from werkzeug import SharedDataMiddleware
import os

if __name__ == '__main__':
    # create app
    app = create_app('sqlite:///app.db', debug=True)

    # route static files, normally the web server takes care of this
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'app/static'),
    })

    # run app
    socketio.run(app, host='127.0.0.1')
