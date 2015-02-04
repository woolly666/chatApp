from flask import Flask, render_template, url_for, request, redirect, flash, session
import pickle
import math, random
import subprocess
import tempfile
import os

app=Flask(__name__)

sender = ""
receiver = ""
encryptDecryptList = []
decryptList = []
n = 0
e = 0
d = 0

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
    
    if request.form['the_comment'] == '':
        all_ok = False
        flash("Sorry you must enter a comment. Try again")
    
    if all_ok:
        set_keys(int(request.form['P']),int(request.form['Q']))
        encryptDecryptList.clear()

        encrypt(request.form['the_comment'],session['n'], session['e'])
        pickle.dump(encryptDecryptList, open(request.form['send_name'] + request.form['receive_name'] + ".txt","wb"))

        return redirect(url_for("getcomment"))
    else:
        return redirect(url_for("getcomment"))


@app.route('/displaycomment')
def showallcomments():
    decryptList.clear()
    try:
        session['encryptDecryptList'] = pickle.load(open(request.form['send_name'] + request.form['receive_name'] + ".txt","rb"))

    except Exception:
        pass

    decrypt(session['d'], session['n'])

    return render_template("show.html",
                            the_title="Here are the current scores",
                            the_data=decryptList,
                            comment_url=url_for("getcomment"))

def set_keys(p,q):
    """This fuction asks for 2 primes. 
    It sets a public key and an encoding number, 'e'."""
    print("\n\nmust be 11 or greater p and q cannot be the same.")
    n = p * q
    mod = (p - 1) * (q - 1)
    e = get_e(mod)
    d = get_d(e, mod)
    while d < 0:
        d += mod
    print("N = ", n,"\nO(",n,")","=",mod,"\ne = ", e, "\nd = ", d)
    session['d'] = d
    session['n'] = n
    session['e'] = e
    return [n, e, d]

def get_e(mod):
    """Finds an e coprime with m."""
    tf = True
    e = random.randint(1, mod)
    
    while gcd(e, mod) != 1:
        e += 1
    return e

def gcd(a,b):
    """Takes two integers and returns gcd."""
    while b > 0:
        a, b = b, a % b
    return a

def get_d(e, m):
    """Takes encoding number, 'e' and the value for 'mod' (p-1) * (q-1).
    Returns a decoding number."""
    x = lasty = 0 
    lastx = y = 1
    while m != 0: 
        q = e // m 
        e, m = m, e % m 
        x, lastx = lastx - q*x, x
        y, lasty = lasty - q*y, y
    return lastx

def encrypt(mess,n, e):
    """This function asks for a message and encodes it using 'n' and 'e'."""
    r = [ord(c) for c in mess]

    for i in r:
        encryptDecryptList.append(pow(i, e, n))
    if not mess:
        return

def decrypt(d, n):
    """This function asks for a number and decodes it using 'd' and 'n'."""
    if not encryptDecryptList:
        print("hello")
        return

    else:
        for i in encryptDecryptList:
            r = pow(i, d, n)
            decryptList.append(chr(r))

app.config['SECRET_KEY'] = 'thisismysecretkeyyouarescrewedmehhehehe' # encrypts/decrypts the session
app.run(debug=True)
