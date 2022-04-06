from flask import Flask 
from threading import Thread 

app = Flask('')

@app.route('/')
def home():
    return '<img src="static/qr.png"> '

def run():
    app.run(host="0.0.0.0", port=8080)

run()
