from flask import Flask, render_template, request, redirect, session, flash, send_file, url_for
import os, shutil
from werkzeug.utils import secure_filename
import DatabaseHelper as db
from FormHelper import RegisterForms, Login
from time import gmtime, strftime
from flask_wtf.csrf import CSRFProtect
from PayTm import Checksum
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_mysqldb import MySQL

UPLOAD_FOLDER = r'Uploaded Documnet//'
ALLOWED_EXTENSIONS = {'pdf'}
csrf = CSRFProtect()
now = strftime("-%Y%m%d-%H%M%S", gmtime())
MERCHANT_KEY = 'lQ5Ypdx5uSdqNsfS'
URL  = URLSafeTimedSerializer("Secreat_key_for_temp_URL")

app = Flask(__name__)
app.config.from_object("config.ProductionConfig")

mail = Mail(app)
mysql = MySQL(app)

def TotalUsers():
    """
        returns tuple number of users and documents in que
    """
    query = "select * from users;"
    cur = mysql.connection.cursor()
    users = cur.execute(query)
    mysql.connection.commit()
    cur.close()

    doc = len(os.listdir("/home/xpressxerox/mysite/Uploaded Documnet//amirkanai01//"))
    print(users, doc)
    return (users, doc)

@app.route('/')
def index():
    """
        route for home page
    """
    (users, doc) = TotalUsers()
    return render_template("home.html", users=users, doc=doc)

def UserRegistration(username, password):
    """
        register user and make directory in system by name of user
    """
    status = "not registrated"
    print("==========username=========",username)
    print("==========password=========",password)
    try:
        query = "Insert Into users(email, password) Values("
        query += "'"+ username + "'," + "'"+ password + "'" + ");"
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        print("==========query executed=========")
        status = "Registration successful"
        user_sub = username.split("@")[0]
        os.mkdir( UPLOAD_FOLDER + user_sub)
        print("-----folder created successfully----", UPLOAD_FOLDER + user_sub)
    except Exception as e:
        print("----Exception is ----",e)
        status = "Exception"

    finally:
        return status

def isUser(email):
    """
        checks email id present or not
    """
    if email == None:
        print("you are none")
        return False
    query = "Select email from  users where email = '" + email + "';"
    cur = mysql.connection.cursor()
    cur.execute(query)
    res = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    if res is not None:
        return True
    else:
        return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForms(request.form)
    if request.method == 'POST' and form.validate():
        if isUser(request.form['email']):
            flash(u"Username is already taken", 'alert alert-secondary')
            return redirect("/register")
        status = UserRegistration(request.form['email'], request.form['password'])
        if status == "Registration successful":
            return redirect("/login")

        elif status == "Exception":
            flash(u" ----ASK ADMIN TO RESTART SERVER---- ", 'alert alert-warning')
            return redirect("/register")

        else:
            flash(u" ----You are missing something---- ", 'alert alert-warning')
            return redirect("/register")
    return render_template("register.html", form=form)


def LogIn(username, password):      # log in user
    status = "not successful"
    res = ""
    try:
        query = "Select * from  users where email = '"
        query += username
        query += "' and password ='"
        query += password
        query += "'"
        print(query)
        cur = mysql.connection.cursor()
        cur.execute(query)
        res = cur.fetchone()
        mysql.connection.commit()
        cur.close()

        if res is not None:
            status = "LogIn successful"

    except Exception as e:
        print("----Exception is ----",e)
        status = "Exception"

    finally:
        print("status from databasehelper ", status)
        return status


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)

    if request.method == 'POST' and form.validate():
        session.pop('username', None)
        user = request.form['email']
        session["username"] = request.form['email']
        print("--------------------current user ", session["username"])
        status = LogIn(request.form['email'], request.form['password'])

        if status == "LogIn successful":

            if user == "amirkanai01@gmail.com":
                return redirect("/admin")
            elif isUser(session["username"]):
                return redirect("/user")

        elif status == "Exception":
            flash(u" ----ASK ADMIN TO RESTART SERVER---- ", 'alert alert-warning')
            return redirect("/login")

        else:
            flash(u' ----Wrong username or password---- ', 'alert alert-danger')
            return redirect("/login")
    else:
        return render_template("LogIn.html", form=form)

@app.route('/forgetPassword', methods=['GET', 'POST'])
def forgetPassword():
    if request.method == "POST":
        email = request.form['email']
        token = URL.dumps(email, salt="email_confirm")
        msg = Message("XpressXerox Change Password", sender="xpressxeroxx@gmail.com", recipients=[email])
        try:
            link = url_for("change", token=token, _external=True)
            msg.body = "Click here to change password \n" + link + "\n"
            mail.send(msg)
            print("----\n", msg, "\n----")
            flash(u" ----Send mail to your mail id---- ", 'alert alert-warning')
            return redirect("/login")
        except Exception as ex:
            print("something went wrong", ex)
            flash(u" ----something went wrong---- ", 'alert alert-warning')
            return redirect("/login")
    return render_template("forgetPassword.html")

@app.route('/change/<token>', methods = ["GET", "POST"])
def change(token):
    try:
        email = URL.loads(token, salt="email_confirm", max_age=360)
        if(request.method == "POST"):
            email = request.form['email']
            password = request.form['password']
            status = changePassword(email, password)
            if status == True:
                flash(u" ----Password changed successfully---- ", 'alert alert-success')
                return redirect("/login")
            else:
                flash(u" ----We are facing some issue ---- ", 'alert alert-success')
                return redirect("/login")

        else:
            return render_template("ChangePassowrd.html", email = email)
    except:
        return "something went wrong"

def changePassword(username, password):
    """
        change password in database
    """
    status = False
    try:
        username = "'" + username + "'"
        password = "'" + password + "'"
        query = " Update users set password = {} where email = {} ;".format(password, username)
        print(query)
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        print("==========query executed=========")
        status = True
    except Exception as e:
        print("----Exception is ----",e)
        status = "Exception"

    finally:
        return status



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/login")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/user', methods=['GET', 'POST'])
def user():
    session["bill"] = 0
    if ((session["username"] != "amirkanai01@gmail.com") and isUser(session["username"])):

        files = db.fileUploded(UPLOAD_FOLDER + session["username"].split("@")[0] )
        print("files-----", files)
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part', "alert alert-primary")
                return redirect(request.url)
            files_uploaded = request.files.getlist("file")
            # print("----files_uploaded---- ", files_uploaded)
            for file in files_uploaded:
                if file.filename == '':
                    flash('No selected file', "alert alert-primary")
                    return redirect(request.url)

                if file and allowed_file(file.filename):
                    pass
                else:
                    flash('WE ACCEPT PDF FILES ONLY', "alert alert-danger")
                    return redirect('/user')
            session["temp_file"] = []
            for file in files_uploaded:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER  + session["username"].split("@")[0] + "//", filename))
                session["temp_file"].append(filename)
                amount = db.pageCounter(UPLOAD_FOLDER  + session["username"].split("@")[0] + "//" + filename)
                session["bill"] += amount
            print("final bill----- ", session["bill"])
            data_dict = {'MID': 'VeMuWi85833969814381', 'TXN_AMOUNT': str(session["bill"]), 'ORDER_ID': session["username"] + now,
                         'CUST_ID': session["username"], 'INDUSTRY_TYPE_ID': 'Retail', 'WEBSITE': 'worldpressplg',
                         'CHANNEL_ID': 'WEB',
                         'CALLBACK_URL': 'http://xpressxerox.pythonanywhere.com/handleRequest', }
            data_dict["CHECKSUMHASH"] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)

            return render_template("PayTm.html", data_dict=data_dict)
        else:
            return render_template("UserDashboard.html", files=files, user = session["username"])
    else:
        flash('Need to Sign In', "alert alert-danger")
        return redirect("/login")

@app.route('/handleRequest', methods=('GET', 'POST'))
@csrf.exempt
def handleRequest():
    form = request.form
    response_dict = dict()
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict["RESPCODE"] == "01":
            print("Money Transfered")
        else:
            files = db.fileUploded(UPLOAD_FOLDER + session["username"].split("@")[0])
            print("files after  uploading handle request ------", files)
            print("files which are uploading----", session["temp_file"])
            for file in session["temp_file"]:
                # filename = file.filename
                # filename = filename.replace(" ","_")
                print(file,  "condition ", file in files)
                if file in files:
                    print("file path ",UPLOAD_FOLDER + session["username"].split("@")[0] + file)
                    os.remove(UPLOAD_FOLDER + session["username"].split("@")[0] + "//" + file)
                    print("file removed")
            print("Problem during transaction ", response_dict["RESPMSG"])

    return render_template("Status.html", response_dict=response_dict, user = session["username"])


@app.route('/action', methods=['POST', 'GET'])
def action():
    if ((session["username"] != "amirkanai01@gmail.com") and isUser(session["username"]) and request.args.get("act") != None):
        status = request.args.get("act")
        file = request.args.get("doc")
        now = strftime("-%Y%m%d-%H%M%S", gmtime())
        temp = session["username"].split("@")[0] + str(now) + "." + file.split(".")[-1]
        if status == "print":
            shutil.move(UPLOAD_FOLDER + session["username"].split("@")[0] + "//" + file , UPLOAD_FOLDER + 'amirkanai01//' + temp)
            return redirect("/user")
        else:
            os.remove(UPLOAD_FOLDER + session["username"].split("@")[0] + "//" + file)
            return redirect("user")
    else:
        return redirect("/login")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session["username"] == "amirkanai01@gmail.com":
        files = db.fileUploded(UPLOAD_FOLDER +  session["username"].split("@")[0])
        return render_template("AdminDashboard.html", files=files, user = session["username"])
    else:
        return redirect("/login")

@app.route('/adminAction', methods=['POST', 'GET'])
def adminAction():
    if ((session["username"] == "amirkanai01@gmail.com") and (request.args.get("act") != None)):
        status = request.args.get("act")
        bill = r'Uploaded Documnet//amirkanai01//----bill----.xlsx'
        files = sorted(db.fileUploded(UPLOAD_FOLDER + session["username"].split("@")[0]))
        if status == "print":
            db.createBillExcel(bill)
            files = sorted(db.fileUploded(UPLOAD_FOLDER + session["username"].split("@")[0]))
            users = []
            record = dict()
            for i in range(1, len(files)):
                file = files[i]
                temp = file.split("-")[0]
                pages = db.pageCounter(UPLOAD_FOLDER + session["username"].split("@")[0] + "//" + file)
                if temp in record:
                    record[temp] += pages
                else:
                    record[temp] = pages

                if temp not in users:
                    users.append(temp)
            print("sqeuence of users ", users)
            print("record dict ", record)
            db.updatedBill(bill, users, record)
            db.createZip(UPLOAD_FOLDER + session["username"].split("@")[0] + "//", files)
            db.deleteFiles(UPLOAD_FOLDER + session["username"].split("@")[0] + "//")
            return send_file('Document.zip', mimetype='zip', attachment_filename='Document.zip', as_attachment=True)

        return render_template("AdminDashboard.html", files = files)
    else:
        return redirect("/login")


if __name__ == "__main__":
    app.run()


