from flask import Flask
from threading import Thread
import schedule
import time
import os
import sys

app = Flask('')


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    try:
        app.run(host='0.0.0.0', port=8080)
    except:
        print("unexcepted error")


def keep_alive():
    t = Thread(target=run)
    t.start()
