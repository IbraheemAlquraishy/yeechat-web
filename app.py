from flask import Flask,redirect,url_for,send_file,abort
import json
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from os import path
from flask import render_template
from flask import request
from views import views
from flask_login import login_user,logout_user,login_required,current_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_socketio import SocketIO,join_room,leave_room,send

app=Flask(__name__)
app.register_blueprint(views,url_prefix="/")
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='hihihihihiekjfakldjflka'
socketiO=SocketIO(app)
db=SQLAlchemy(app)

user_room=db.Table('user_room',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('room_id',db.Integer,db.ForeignKey('room.id'))
)


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(124),unique=True,nullable=False)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    img=db.Column(db.String(200),nullable=False,default='uploads/default.png')
    #publickey=db.Column(db.String(1024),nullable=False)
    #mes=db.relationship('Message',lazy=True)
    joined=db.relationship('Room',secondary=user_room,backref='members')

    def __repr__(self):
        return f"user('{self.name}','{self.id}')"

class Room(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Room):
            return {"id": obj.id, "name": obj.name}
        elif isinstance(obj, User):
            return {"name":obj.username,"photo":obj.img}
        return super().default(obj)

if not path.exists("yeechat-web/database.db"):
    with app.app_context():   
        db.create_all()


l=login_manager.LoginManager()
l.login_view='login'
l.init_app(app)
@l.user_loader
def load_user(id):
    return User.query.get(int(id))

def haveperm(rid):
    room=Room.query.filter_by(id=rid).first()
    for i in range(len(room.members)):
       if current_user.id ==room.members[i].id:
           return True
    return False
    



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
    username=request.json.get('username')
    passwrd=request.json.get('password')
    if User.query.filter_by(name=name).first()==None:
        user=User(name=name,username=username,password=generate_password_hash(passwrd,method='sha256'))
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=True)
        return '{"message":"done"}'
    else:
        return '{"message":"taken"}'

@app.route("/chats")
@login_required
def chat():
    return render_template("chats.html",user=current_user)

@app.route("/chats/create",methods=['POST'])
@login_required
def create():
    name=request.json.get("name")
    user=request.json.get("user")
    if User.query.filter_by(name=user).first()==None:
        return '{"message":"no such user"}'
    else:
        room=Room(name=name)
        db.session.add(room)
        db.session.commit()
        current_user.joined.append(room)
        u=User.query.filter_by(name=user).first()
        u.joined.append(room)
        db.session.commit()
        return '{"message":"done"}'

@app.route("/chats/available",methods=['GET'])
@login_required
def available():
    rooms_id=current_user.joined
    body='{"rooms":'
    body_json=json.dumps(rooms_id,cls=MyEncoder)
    body+=body_json+'}'
    return body

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
@app.route("/uploads/<url_endpoint>")
@login_required
def getimg(url_endpoint):
    return send_file('uploads/'+url_endpoint)

@app.route("/chats/<url_endpoint>")
@login_required
def chatend(url_endpoint):
    if haveperm(url_endpoint):
        return render_template("test.html")
    else:
        abort(403)


@socketiO.on("connect")
def connect(auth):
    return "ok"
@socketiO.on("connect_chat")
def connect_chat(js):
    print("connect to" +js["chat_id"])
    if haveperm(js["chat_id"]):
        room=Room.query.filter_by(id=js["chat_id"]).first()
        join_room(room)
        body_json=json.dumps(room.members,cls=MyEncoder)
        socketiO.emit("chat_members",{"users":body_json})

@socketiO.on('message')
def remessage(js):
    print(js['data'])

@socketiO.on("client_message")
def disconnect(js):
    room=Room.query.filter_by(id=js["chat_id"]).first()
    leave_room(room)
    print("leave "+room.id)

if __name__=='__main__':
    
    socketiO.run(app,debug=True,port=3000)


