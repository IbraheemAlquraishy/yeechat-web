from app import db
import datetime
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(124),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    img=db.Column(db.String(200),nullable=False,default='uploads/default.default.png')
    #publickey=db.Column(db.String(1024),nullable=False)
    #mes=db.relationship('Message',lazy=True)
    

    def __repr__(self):
        return f"user('{self.name}','{self.publickey}')"

# class Message(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     data=db.Column(db.string,nullable=False)
#     sender_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     time=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    
