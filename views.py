from flask import Blueprint
from flask import render_template
from flask import request
views=Blueprint(__name__,"views")
@views.route("/",methods=['GET'])
def home():
    return render_template("index.html")

@views.route("/login",methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    else:
        name=request.json.get('name')
        passwrd=request.json.get('password')
        if name=="ibraheem" and passwrd=="idk":
            return "done"
        else:
            return "wrong"
        

@views.route("/signup",methods=['GET'])
def getsignup():
    return render_template("signup.html")


    
# error handlers

@views.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@views.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500