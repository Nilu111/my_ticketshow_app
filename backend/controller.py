from flask import Flask,render_template,request
from .models import *
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login' , methods=["GET","POST"])
def login_page():
    if request.method=="POST":
        uname=request.form.get("username")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0:
            return render_template("admin_dashboard.html")
        elif usr and usr.role==1:
            return render_template("user_dashboard.html",user=usr.full_name)
        else:
            return render_template('login.html',msg="Invalid Credentials")
    return render_template("login.html",msg="")


@app.route('/signup', methods=["GET","POST"])
def sighup_page():
    if request.method=="POST":
        uname=request.form.get("username")
        pwd=request.form.get("password")
        full_name=request.form.get("fullname")
        address=request.form.get("location")
        pin_code=request.form.get("pincode")
        usr=User_Info.query.filter_by(email=uname).first()
        if usr:
            return render_template('signup.html',msg="user already existed")
        new_usr=User_Info(email=uname,password=pwd,full_name=full_name,address=address,pin_code=pin_code)
        db.session.add(new_usr)
        db.session.commit()
        return render_template('login.html',msg="Registration done successfully!")
    return render_template('signup.html',msg="")