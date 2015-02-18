from flask import Flask, render_template, url_for, request, redirect, flash, session
import pickle
import math, random
import subprocess
import tempfile
import os

app=Flask(__name__)

sender = ""
receiver = ""
key = ""
encryptDecryptList = []
decryptList = []
n = 0
e = 0
d = 0

@app.route('/')
def display_home(): # home page
    return render_template("home.html",
                            the_title="Welcome to the Commenting System.",
                            login_url=url_for("getLogin"),
                            comment_url=url_for("getcomment"),
                            comment_url2=url_for("getcomment2"),
                            show_url=url_for("showallcomments"))

@app.route('/entercomment')
def getcomment():# enter rsa
    return render_template("enter.html",
                            the_title="Send Message",
                            the_save_url=url_for("saveformdata"),
                            show_link=url_for("showallcomments"))

@app.route('/entercomment2')
def getcomment2():# enter private key
    return render_template("enter2.html",
                            the_title="Send Message",
                            the_save_url=url_for("saveformdata2"),
                            show_link2=url_for("showallcomments2"))

@app.route('/login')
def getLogin(): # display login page
    return render_template("login.html",
                            the_title="Login",
                            register_link=url_for("getRegister"))

@app.route('/register')
def getRegister(): # display register page
    return render_template("register.html",
                            the_title="Register for an account")


@app.route('/email checker', methods = ["POST"])
def emailExist():
    emailList = []
    exists=False
    
    session['firstName'] = request.form["FirstName"]
    session['lastName'] = request.form["LastName"]
    session['userEmail'] = str(request.form["userEmail"])
    session['pass'] = str(request.form["password"])
    session['phone'] = str(request.form["phone"])

    #connection = mariadb.connect(host="localhost",
    #                             user="root",
    #                             password="Jamesh92",
    #                             database="TakeMeThere")

    #getEmail = """SELECT email FROM users""" 
    
   # cursor = connection.cursor()
    
    #cursor.execute(getEmail)
   # emailList =cursor.fetchall()
    
    #connection.commit()
   # connection.close()

    

    for item in emailList:
        print("IN FUNCTION")
        
        if checkEmail == item[0]:
            
            print("IN IF")
            exists = True

    ################ THANK YOU FOR REGISTERING PAGE ######################################################################################################################

    if exists == False:
        print("*********************** FALSE *****************************")
        print("THANKS PAGE ",session.get('firstName'))

       # connection = mariadb.connect(host="localhost",
        #                         user="root",
         #                        password="Jamesh92",
          #                       database="TakeMeThere")
    
        #cursor = connection.cursor()
    
        #cursor.execute(registeringData, (session.get('firstName'),session.get('lastName'),session.get('userEmail'),session.get('pass'),session.get('phone'),))
        #cursor.execute(registerLoc)
    
        #connection.commit()
        #connection.close()

        return render_template("thanks.html",
                           the_title = "Thank You For Registering!", )

################ EMAIL EXISTS ######################################################################################################################

    else:
        print("========================= TRUE ===============================")
       # flash("Sorry This Email Address Already Exists!!!!")
        return render_template("registerFail.html",
                               the_title = "Welcome to the Registration Page!", )




######################################################################################################################


@app.route('/saveform', methods=["POST"])
def saveformdata(): # save for rsa
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
        set_keys(int(request.form['P']),int(request.form['Q']))#set key
        encryptDecryptList.clear()# clear list

        encrypt(request.form['the_comment'],session['n'], session['e'])# encrypt message
        pickle.dump(encryptDecryptList, open(request.form['send_name'] + request.form['receive_name'] + ".txt","wb"))# put in file

        return redirect(url_for("getcomment"))
    else:
        return redirect(url_for("getcomment"))

@app.route('/saveform2', methods=["POST"])
def saveformdata2(): # save for private key
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
        session['key'] = request.form['the_key'] # set key
        encryptDecryptList.clear() # clear list

        encrypt2(request.form['the_comment'],session['key']) # encrypt message
        pickle.dump(encryptDecryptList, open(request.form['send_name'] + request.form['receive_name'] + ".txt","wb")) # put in file

        return redirect(url_for("getcomment2"))
    else:
        return redirect(url_for("getcomment2"))


@app.route('/displaycomment')
def showallcomments(): # show for rsa
    decryptList.clear()
    try:
        session['encryptDecryptList'] = pickle.load(open(request.form['send_name'] + request.form['receive_name'] + ".txt","rb"))
        print(encryptDecryptList)

    except Exception:
        pass

    decrypt(session['d'], session['n']) # decrypt file

    return render_template("show.html",
                            the_title="Here are the current scores",
                            the_data=decryptList,
                            comment_url=url_for("getcomment"))

@app.route('/displaycomment2')
def showallcomments2(): # show for private key
    decryptList.clear()
    try:
        session['encryptDecryptList'] = pickle.load(open(request.form['send_name'] + request.form['receive_name'] + ".txt","rb"))
        print(encryptDecryptList)

    except Exception:
        pass

    decrypt2(session['key'])# decrypt file

    return render_template("show2.html",
                            the_title="Here are the current scores",
                            the_data=decryptList,
                            comment_url=url_for("getcomment2"))

def set_keys(p,q): # set rsa keys
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

def get_e(mod): # get e for rsa
    """Finds an e coprime with m."""
    tf = True
    e = random.randint(1, mod)
    
    while gcd(e, mod) != 1:
        e += 1
    return e

def gcd(a,b): # get gcd for rsa
    """Takes two integers and returns gcd."""
    while b > 0:
        a, b = b, a % b
    return a

def get_d(e, m):# get d for rsa
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

def encrypt(mess,n, e): #rsa encryption
    """This function asks for a message and encodes it using 'n' and 'e'."""    
    r = [ord(c) for c in mess]

    for i in r:
        encryptDecryptList.append(pow(i, e, n))
    if not mess:
        return

def encrypt2(mess, k): # private key encryption
    characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    count = 0
    r = [ord(c) for c in mess]

    for i in r:
        encryptDecryptList.append(i + characters.index(k[count]))
        count = count + 1
        if count == len(k):
           count = 0
    if not mess:
        return


def decrypt(d, n): # rsa decryption
    """This function asks for a number and decodes it using 'd' and 'n'."""
    if not encryptDecryptList:
        return

    else:
        for i in encryptDecryptList:
            r = pow(i, d, n)
            decryptList.append(chr(r))

def decrypt2(k): # private decryption
    characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    count = 0

    if not encryptDecryptList:
        return

    else:
        for i in encryptDecryptList:
            r = (i-characters.index(k[count]))
            count = count + 1
            if count == len(k):
               count = 0
            decryptList.append(chr(r))

app.config['SECRET_KEY'] = 'thisismysecretkeyyouarescrewedmehhehehe' # encrypts/decrypts the session
app.run(debug=True)