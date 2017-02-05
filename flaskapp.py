from datetime import datetime
 
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'iloveeatingsausage'


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
