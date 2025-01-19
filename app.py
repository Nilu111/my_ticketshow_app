from flask import Flask
from backend.models import db

app=None

def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///ticket_shoq.sqlite3"   #having db file
    db.init_app(app) #flask app connectednton db(sqlalchemy)
    app.app_context().push() #direct access to other models like database
    app.debug=True
    print("my_cine_world started...")
    

# call the app

setup_app()
    



from backend.controller import *
if __name__ =="__main__":
    app.run()