from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import login_required,current_user
views=Blueprint(__name__,"views")




@views.route("/",methods=['GET'])
def home():
    return render_template("index.html")


# error handlers

@views.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@views.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500