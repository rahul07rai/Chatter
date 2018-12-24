#!/usr/bin/env python3

import hashlib
from datetime import datetime
from db import add_data, auth, friendList
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
sig1 = None
sig2 = None

def hash(text):
    encrypt = hashlib.sha256()
    encrypt.update(text.encode())
    return encrypt.hexdigest()


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/signin', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        global sig1
        sig1 = request.form['signature']
        passwd = hash(request.form['password'])
        ch = auth(sig1, passwd)
        if ch == 0:
            return redirect(url_for('online'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('signin.html', error=error)


@app.route('/signup', methods=['GET','POST'])
def signup():
    error = None
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '' or request.form['contact'] == '':
            error = 'Invalid Credentials. Please try again.'
        else:
            name = request.form['username']
            passwd = hash(request.form['password'])
            contact = request.form['contact']
            sign = request.form['username'] + request.form['contact']
            timestamp = datetime.now()
            add_data(name, passwd, contact, sign, timestamp)
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)


@app.route('/online_users',methods=['GET','POST'])
def online():
    global sig1
    frnd_list = friendList(sig1)
    if request.method == 'POST':
        global sig2
        sig2 = request.form['sign2']
        return redirect(url_for('chat'))
    return render_template('online_users.html', frnd_list=frnd_list, sign=sig1)
    

@app.route('/chat', methods=['GET','POST'])
def chat():
    global sig1
    global sig2
    msg = None
    if request.method == 'POST':  
        msg = request.form['text']
    return render_template('chat.html', name1=sig1, msg=msg)


if __name__ == '__main__':
    app.run()

