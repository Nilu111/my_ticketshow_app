from flask import Flask,render_template,request,url_for,redirect
from .models import *
from flask import current_app as app
from datetime import datetime


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
            return redirect(url_for("admin_dashboard",name=usr.full_name))
        elif usr and usr.role==1:
            return redirect(url_for("user_dashboard",name=usr.full_name))
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

@app.route("/admin/<name>")
def admin_dashboard(name):
    theatres =get_theatres()
    return render_template("admin_dashboard.html",name=name,theatres=theatres)


@app.route("/user/<name>")
def user_dashboard(name):
    return render_template("user_dashboard.html",name=name)



@app.route('/venue/<name>',methods=["GET","POST"])
def add_venue(name):
    if request.method=="POST":
        vname=request.form.get('theater_name')
        location=request.form.get('location')
        pincode=request.form.get('pincode')
        capacity=request.form.get('capacity')
        new_theater=Theatre(name=vname,location=location,pin_code=pincode,capacity=capacity)
        db.session.add(new_theater)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
        
    return render_template("add_venue.html",name=name)


@app.route('/show/<venue_id>/<name>',methods=["GET","POST"])
def add_show(venue_id,name):
    if request.method=="POST":
        sname=request.form.get('show_name')
        tags=request.form.get('tags')
        tkt_price=request.form.get('tkt_price')
        date_time=request.form.get('date_time')
        dt_time=datetime.strptime(date_time,"%Y-%m-%dT%H:%M")
        new_show=Show(name=sname,tags=tags,ticket_price=tkt_price,date_time=dt_time,theatre_id=venue_id)
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    
    return render_template("add_show.html",name=name,venue_id=venue_id)


@app.route("/search/<name>", methods=['GET','POST'])
def search(name):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        by_venue = search_by_venue(search_txt)
        by_location = search_by_location(search_txt)
        if by_venue:
            return render_template("admin_dashboard.html",name=name,theatres=by_venue)
        elif by_location :
            return render_template("admin_dashboard.html",name=name,theatres=by_location)


    return redirect(url_for("admin_dashboard",name=name))


def search_by_venue(search_txt):
    theateres = Theatre.query.filter(Theatre.name.ilike(f"%{search_txt}%")).all()
    return theateres

def search_by_location(search_txt):
    theateres = Theatre.query.filter(Theatre.location.ilike(f"%{search_txt}%")).all()
    return theateres





def get_theatres():
    theatres=Theatre.query.all()
    return theatres