import os
import signal
from flask import Flask
import innApi

app = Flask(__name__)

signal.signal(signal.SIGINT, lambda s, f: os._exit(0))

@app.route("/")
def mainn():
    page = '<html><body><h1>'
    page += innApi.mainn()
    page += '</h1></body></html>'
    return page

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT')) # port 5000 is the default
