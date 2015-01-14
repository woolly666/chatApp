from flask import Flask, render_template, url_for, request, redirect, flash, session
import subprocess
import tempfile
import os

app=Flask(__name__)

sender = ""
receiver = ""

@app.route('/')
def display_home():
    return render_template("home.html",
                            the_title="Welcome to the Commenting System.",
                            login_url=url_for("getLogin"),
                            comment_url=url_for("getcomment"),
                            show_url=url_for("showallcomments"))

@app.route('/entercomment')
def getcomment():
    return render_template("enter.html",
                            the_title="Send Message",
                            the_save_url=url_for("saveformdata"),
                            show_link=url_for("showallcomments"))

@app.route('/login')
def getLogin(): # display login page
    return render_template("login.html",
                            the_title="Login",
                            register_link=url_for("getRegister"))

@app.route('/register')
def getRegister(): # display register page
    return render_template("register.html",
                            the_title="Register for an account")

@app.route('/saveform', methods=["POST"])
def saveformdata():
    all_ok = True
    if request.form['send_name'] == '':
        all_ok = False
        flash("Sorry you must tell me your name. Try again")
    
    if request.form['receive_name'] == '':
        all_ok = False
        flash("Sorry you must tell me your name. Try again")
    print('-->', request.form['the_comment'], '<--')
    
    if request.form['the_comment'] == '':
        all_ok = False
        flash("Sorry you must enter a comment. Try again")
    
    if all_ok:
        with open(request.form['send_name'] + request.form['receive_name'] + ".txt",'a') as log:
            print(request.form['send_name'], 'said', file=log)
            print(request.form['the_comment'], file=log)
            session['sender'] = request.form['send_name']
            session['receiver'] = request.form['receive_name']
        return redirect(url_for("getcomment"))

    else:
        return redirect(url_for("getcomment"))


@app.route('/displaycomment')
def showallcomments():
    with open(session['sender'] + session['receiver'] + ".txt") as log:
        lines = log.readlines()
    return render_template("show.html",
                            the_title="Chat Window",
                            the_data=lines,
                            comment_url=url_for("getcomment"))

app.config['SECRET_KEY'] = 'thisismysecretkeyyouarescrewedmehhehehe' # encrypts/decrypts the session
app.run(debug=True)
