import os
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps
import jwt
import datetime
from werkzeug.security import generate_password_hash,check_password_hash

from flask import jsonify

db = SQLAlchemy()
app = Flask(__name__)


#create connection
mysqlHost = os.getenv('MYSQL_HOST', default='localhost')
mysqlPort = os.getenv('MYSQL_PORT', default='3306')
mysqlUser = os.getenv('MYSQL_USER', default='cabl')
mysqlPassword = os.getenv('MYSQL_PASSWORD', default='cabl')
mysqlDatabase = os.getenv('MYSQL_DATABASE', default='cabl')
app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{mysqlUser}:{mysqlPassword}@{mysqlHost}:{mysqlPort}/{mysqlDatabase}"
db.init_app(app)

#### Database Objects #######
Base = declarative_base()
# class UserGroupLink(Base):
#   __tablename__ = 'cable_user_group'
#   groupName = db.Column(db.String(255), db.ForeignKey('Group.name'), primary_key=True)
#   userName = db.Column(db.String(255), db.ForeignKey('User.username'), primary_key=True)

class Location (db.Model):
  __tablename__ = 'cabl_location'
  name = db.Column(db.String(255), primary_key=True)
  is_disabled=db.Column(db.Boolean)

# class Group(db.Model):
#   __tablename__ = 'cabl_group'
#   name = db.Column(db.String(255), primary_key=True )
#   is_disabled = db.Column(db.Boolean)
#   users = db.relationship("User", secondary='cable_user_group')

class User(db.Model):
  __tablename__ = 'cabl_user'
  username = db.Column(db.String(255), unique=True )
  password = db.Column(db.String(255))
  email = db.Column(db.String(255), primary_key=True)
  location = db.Column(db.String(255), db.ForeignKey("cabl_location.name"))
  # groups = db.relationship("Group",secondary='cable_user_group')

  def as_dict(self):
    return {"username": self.username, "email": self.email , "location": self.location}



#### JWT  ##########
def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None
    if 'Authorization' in request.headers:
      token = request.headers['Authorization']

    if not token:
      return jsonify({'message': 'a valid token is missing'}), 404
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
      current_user = User.query.filter_by(email=data['email']).first()
    except:
      return jsonify({'message': 'token is invalid'}), 400

    return f(current_user, *args, **kwargs)
  return decorator


######   API Defintion #######

@app.route('/users', methods=['GET'])
@token_required
def getUsers():
  # if request.method == 'POST':
  users = User.query.all()
  userList = []
  for user in users:
    userList.append(user.as_dict())
  return jsonify(userList)

@app.route('/user', methods=['POST'])
#@token_required
def createUser():
  # if request.method == 'POST':
  user = User(
    username=request.form["username"],
    email=request.form["email"],
    location=request.form["location"],
    password=generate_password_hash (request.form["password"], method='sha256')
  )
  db.session.add(user)
  db.session.commit()
  return "user created",201

@app.route('/login', methods=['POST'])
def login():
  parameter = request.get_json()
  email = parameter["email"]
  password = parameter["password"]

  user = User.query.filter_by(email=email).first()
  if check_password_hash(user.password, password):
    token = jwt.encode(
      {'username': user.username, 'email':user.email, 'location': user.location, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
      app.config['SECRET_KEY'], "HS256")

    return jsonify({'token': token, 'email': user.email, 'username': user.username, 'location': user.location})
  return 'error', 401


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
    #Base.metadata.create_all(db.engine)
  app.run(debug=True, host="0.0.0.0")