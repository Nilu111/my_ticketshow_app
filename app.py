from flask import Flask,render_template

app=None

def setup_app():
    app=Flask(__name__)
    app.app_context().push() #direct access to other models like database
    # from models/sqlite connection
    app.debug=True
    print("my_cine_world started...")\
    

# call the app

setup_app()
    



from backend.controller import *

app.run()