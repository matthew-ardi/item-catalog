#!/usr/bin/env python
from app import app

if __name__ == '__main__':
    # app = config.app
    app.secret_key = 'dkwkdo390fl201d0xl3kd'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
