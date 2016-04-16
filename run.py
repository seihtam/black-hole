#!/usr/bin/env python
from app import create_app, socketio

if __name__ == '__main__':
    # create app
    app = create_app('sqlite:///app.db', debug=True)

    # run app
    socketio.run(app, host='127.0.0.1')
