from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from os import path
from flask import render_template
from flask import request
from views import views
from flask_login import login_user,logout_user,login_required,current_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.register_blueprint(views,url_prefix="/")
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='hihihihihiekjfakldjflka'

db=SQLAlchemy(app)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(124),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    img=db.Column(db.String(200),nullable=False,default='uploads/default.default.png')
    #publickey=db.Column(db.String(1024),nullable=False)
    #mes=db.relationship('Message',lazy=True)
    

    def __repr__(self):
        return f"user('{self.name}','{self.publickey}')"

if not path.exists("yeechat-web/database.db"):
    with app.app_context():   
        db.create_all()


l=login_manager.LoginManager()
l.login_view='login'
l.init_app(app)
@l.user_loader
def load_user(id):
    return User.query.get(int(id))

#this is here and not in views because of an error 
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    else:
        name=request.json.get('name')
        passwrd=request.json.get('password')
        user=User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, passwrd):
                login_user(user,remember=True)
                return '{"message":"ok"}'
            else:
                return '{"message":"wrong"}'
        else:
            return '{"message":"wrong"}'
        

@app.route("/signup",methods=['POST'])
def getsignup():
    name=request.json.get('name')
    passwrd=request.json.get('password')
    if User.query.filter_by(name=name).first()==None:
        user=User(name=name,password=generate_password_hash(passwrd,method='sha256'))
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=True)
        return '{"message":"done"}'
    else:
        return '{"message":"taken"}'
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

if __name__=='__main__':
    
    app.run(debug=True,port=3000)


