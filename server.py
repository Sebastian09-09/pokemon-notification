from flask import Flask 

app = Flask('')

@app.route('/')
def home():
    return '<img src="static/qr.png"> '

def run():
    app.run()

run()
