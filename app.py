from flask import Flask,redirect,url_for,send_file,abort
import json
import enc
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
    db.Column('room_id',db.Integer,db.ForeignKey('room.id')),
    db.Column('user_role',db.Integer)
)



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(124),unique=True,nullable=False)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    img=db.Column(db.String(200),nullable=False,default='uploads/default.png')
    tag=db.Column(db.String,nullable=False)
    nonce=db.Column(db.String,nullable=False)
    privetkey=db.Column(db.String(2048),nullable=False)
    publickey=db.Column(db.String(2048),nullable=False)
    mes=db.relationship('Message',lazy=True)
    joined=db.relationship('Room',secondary=user_room,backref='members')
    au=db.relationship('Authnkey',lazy=True)
    def __repr__(self):
        return f"user('{self.name}','{self.id}')"

class Room(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    mes=db.relationship('Message',lazy=True)
    au=db.relationship('Authnkey',lazy=True)

class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.String,nullable=False)
    sender_name=db.Column(db.Integer,db.ForeignKey('user.name'),nullable=False)
    room_id=db.Column(db.Integer,db.ForeignKey('room.id'),nullable=False)
    time=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    tag=db.Column(db.String,nullable=False)
    nonce=db.Column(db.String,nullable=False)
    def dec(key):
        return enc.decry(key,data,nonce,tag).decode()
class Authnkey(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.String,nullable=False)
    room_id=db.Column(db.Integer,db.ForeignKey('room.id'),nullable=False)
    sender_name=db.Column(db.Integer,db.ForeignKey('user.name'),nullable=False)
class MyEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key', None)
        super().__init__(*args, **kwargs)
    
    def default(self, obj):
        if isinstance(obj, Room):
            return {"id": obj.id, "name": obj.name}
        elif isinstance(obj, User):
            return {"name":obj.username,"photo":obj.img}
        elif isinstance(obj,Message):
            time=obj.time
            ntime=time.isoformat()
            return {"name":obj.sender_name,"data":enc.decry(self.key,obj.data,obj.nonce,obj.tag).decode(),"time":ntime}
        return super().default(obj)

if not path.exists("yeechat-web/database.db"):
    with app.app_context():   
        db.create_all()


l=login_manager.LoginManager()
l.login_view='login'
l.init_app(app)

keys={}

def getpri(user,key):
    return enc.decry(key, user.privetkey,user.nonce,user.tag)

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
                key=enc.createkey(passwrd)
                keys[user.id]=key
                print(keys[user.id])
                
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
        key=enc.createkey(passwrd)
        pri,pub=enc.creatersakey()
        c,n,t=enc.encry(key, pri)
        user=User(name=name,username=username,password=generate_password_hash(passwrd,method='sha256'),tag=t,nonce=n,privetkey=c,publickey=pub)
        db.session.add(user)
        db.session.commit()
        keys[user.id]=key
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
        current_user.joined.append(room)
        authkey=enc.createsessionkey()
        authnkey=Authnkey(data=enc.encrsa(current_user.publickey,authkey),room_id=room.id,sender_name=current_user.name)
        db.session.add(authnkey)
        u=User.query.filter_by(name=user).first()
        u.joined.append(room)
        authnkey=Authnkey(data=enc.encrsa(u.publickey,authkey),room_id=room.id,sender_name=u.name)
        db.session.add(authnkey)
        db.session.execute(user_room.update().values(user_role=0).where(user_room.c.user_id == current_user.id).where(user_room.c.room_id == room.id))
        db.session.commit()
        db.session.execute(user_room.update().values(user_role=2).where(user_room.c.user_id == u.id).where(user_room.c.room_id == room.id))
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

@app.route("/chats/<url_endpoint>/add",methods=["POST"])
@login_required
def addmember(url_endpoint):
    if haveperm(url_endpoint):
        room=Room.query.filter_by(id=url_endpoint).first()
        user=User.query.filter_by(name=request.json.get("name")).first()
        pri=getpri(current_user,keys[current_user.id])
        authkey=Authnkey.query.filter_by(sender_name=current_user.name,room_id=url_endpoint).first()
        authkey=enc.decrsa(pri,authkey.data)
        authnkey=Authnkey(data=enc.encrsa(user.publickey,authkey),sender_name=user.name,room_id=url_endpoint)
        db.session.add(authnkey)
        print(request.json.get("name"))
        user.joined.append(room)
        db.session.execute(user_room.update().values(user_role=2).where(user_room.c.user_id == user.id).where(user_room.c.room_id == room.id))
        db.session.commit()
        return {"message":"done"}
    else:
        return {"message":"you dont have access"}

@app.route("/chats/<url_endpoint>/role")
@login_required
def myrole(url_endpoint):
    if haveperm(url_endpoint):
        role = db.session.query(user_room.c.user_role).filter(user_room.c.user_id == current_user.id, user_room.c.room_id == url_endpoint).scalar()
        return {"role":role}
    else:
        return {"message":"you dont have access"}

@socketiO.on("connect")
def connect(auth):
    return "ok"
@socketiO.on("connect_chat")
def connect_chat(js):
    print("connect to" +js["chat_id"])
    if haveperm(js["chat_id"]):
        room=Room.query.filter_by(id=js["chat_id"]).first()
        join_room(room)
        authkey=Authnkey.query.filter_by(sender_name=current_user.name,room_id=room.id).first()
        authnkey=enc.decrsa(getpri(current_user,keys[current_user.id]),authkey.data)
        encoder=MyEncoder(key=authnkey)
        mes_json=encoder.encode(room.mes)
        body_json=json.dumps(room.members,cls=MyEncoder)
        socketiO.emit("chat_members",{"users":body_json,"messages":mes_json},to=request.sid)

@socketiO.on('message')
def message(js):
    print(js['data'])
    if(haveperm(js['room'])):
        authkey=Authnkey.query.filter_by(sender_name=current_user.name,room_id=js['room']).first()
        authnkey=enc.decrsa(getpri(current_user,keys[current_user.id]),authkey.data)
        data,nonce,tag=enc.encry(authnkey,js['data'].encode())
        mes=Message(data=data,sender_name=current_user.name,room_id=js['room'],nonce=nonce,tag=tag)
        db.session.add(mes)
        db.session.commit()
        encoder=MyEncoder(key=authnkey)
        body_json=encoder.encode(mes)
        print(body_json)
        socketiO.emit('message',body_json)
    else:
        return


if __name__=='__main__':
    
    socketiO.run(app,debug=True,port=3000)


