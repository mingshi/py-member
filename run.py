#!/usr/bin/env python
# -*- coding: utf-8 -*-
from member import app

if __name__ == "__main__":
    if app.config['DEBUG'] :
        print app.config

    #app.run(host=app.config['HOST'], port=app.config['PORT'])
    app.run()
