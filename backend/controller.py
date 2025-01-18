from flask import Flask,render_template
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def sighup_page():
    return render_template('signup.html')