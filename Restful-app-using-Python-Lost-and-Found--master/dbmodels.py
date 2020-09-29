from dbconnect import *
#from passlib.apps import custom_app_context as pwd_context




#MODEL
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(200))
    product = db.relationship('Product', backref='user')

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id



class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(200))
    location = db.Column(db.String(200))
    Date = db.Column(db.String(200))
    Status = db.Column(db.String(10))
    Images = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self,name,description,location,Date,status,user_id):
        self.name = name
        self.description = description
        self.location = location
        self.Date = Date
        self.Status = status
        self.user_id = user_id


#model schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'description','location', 'Date', 'Status','user_id')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username', 'password')

#init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

