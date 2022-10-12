import os

import uuid
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


# database connection
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

class Case (db.Model):
  _tablename__ = 'cabl_cases'
  id = db.Column(db.Integer,  primary_key=True )
  datum = db.Column(db.String(255))
  volljaerig = db.Column(db.String(255))
  geschlecht = db.Column(db.String(255))
  wohnsituation = db.Column(db.String(255))
  wohnsituation_zusatz = db.Column(db.String(255))
  aufenthaltstatus = db.Column(db.String(255))
  aufenthaltstatus_zusatz = db.Column(db.String(255))
  krankenversicherung = db.Column(db.String(255))
  notvallv = db.Column(db.String(255))
  medivers = db.Column(db.String(255))
  fachbereich = db.Column(db.String(255))
  fachbereich_zusatz = db.Column(db.String(255))
  location = db.Column(db.String(255), db.ForeignKey("cabl_location.name"), nullable=True)

  def as_dict(self):
    return {"id": self.id,
            "datum": self.datum ,
            "volljaerig": self.volljaerig,
            "geschlecht": self.geschlecht,
            "wohnsituation": self.wohnsituation,
            "wohnsituation_zusatz": self.wohnsituation_zusatz,
            "aufenthaltstatus": self.aufenthaltstatus,
            "aufenthaltstatus_zusatz": self.aufenthaltstatus_zusatz,
            "krankenversicherung": self.krankenversicherung,
            "notvallv": self.notvallv,
            "fachbereich": self.fachbereich,
            "fachbereich_zusatz": self.fachbereich_zusatz,
            "location": self.location}


class Location (db.Model):
  __tablename__ = 'cabl_location'
  name = db.Column(db.String(255), primary_key=True)
  is_disabled=db.Column(db.Boolean)

  def as_dict(self):
    return {"name": self.name, "is_disabled": self.is_disabled }


class User(db.Model):
  __tablename__ = 'cabl_user'
  username = db.Column(db.String(255), unique=True )
  password = db.Column(db.String(255))
  email = db.Column(db.String(255), primary_key=True)
  location = db.Column(db.String(255), db.ForeignKey("cabl_location.name"), nullable=True)
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
      print ("Received Token: ", token)

    if not token:
      return jsonify({'message': 'a valid token is missing'}), 404
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
      current_user = User.query.filter_by(email=data['email']).first()
      print ("Detected User: ", current_user)
    except:
      return jsonify({'message': 'token is invalid'}), 400

    return f(current_user, *args, **kwargs)
  return decorator


######   API Defintion   #######

###  USER API  ###

@app.route('/users', methods=['GET'])
@token_required
def getUsers(loggedInUser):
  users = User.query.all()
  userList = []
  for user in users:
    userList.append(user.as_dict())
  return jsonify(userList)

@app.route('/user', methods=['POST', 'DELETE'])
@token_required
def handleUser(loggedInUser):
  content = request.get_json()
  if request.method == 'POST':
    user = User(
      username=content["username"],
      email=content["email"],
      location=content["location"] if "location" in content else None,
      password=generate_password_hash (content["password"], method='sha256')
    )
    db.session.add(user)
    db.session.commit()
    return "user created",201
  elif request.method == 'DELETE':
    user = User.query.filter_by(email=content['email']).first()
    if user is not None:
      db.session.delete(user)
      db.session.commit()
      return "user deleted", 200
    else: return "user not found", 404

###  CASE API  ###

@app.route('/cases', methods=['GET'])
@token_required
def getCases(loggedInUser):
  cases = Case.query.all()
  caseList = []
  for case in cases:
    caseList.append(case.as_dict())
  return jsonify(caseList)


@app.route('/case', methods=['POST', 'DELETE'])
@token_required
def handleCase(loggedInUser):
  content = request.get_json()
  if request.method == 'POST':
    case = Case(
      datum=content.datum,
      volljaerig=content.volljaerig,
      geschlecht=content.geschlecht,
      wohnsituation=content.wohnsituation,
      wohnsituation_zusatz=content.wohnsituation_zusatz,
      aufenthaltstatus=content.aufenthaltstatus,
      aufenthaltstatus_zusatz=content.aufenthaltstatus_zusatz,
      krankenversicherung=content.krankenversicherung,
      notvallv=content.notvallv,
      fachbereich=content.fachbereich,
      fachbereich_zusatz=content.fachbereich_zusatz,
      location=content.location
    )
    db.session.add(case)
    db.session.commit()
    return "case created",201
  elif request.method == 'DELETE':
    case= Case.query.filter_by(id=content['id']).first()
    if case is not None:
      db.session.delete(case)
      db.commit
      return "case deleted", 200
    else: return "case not found", 404

@app.route('/login', methods=['POST'])
def login():
  content = request.get_json()
  email = content["email"]
  password = content["password"]

  user = User.query.filter_by(email=email).first()
  if user is None:
    return 'user or password incorrect', 401
  if check_password_hash(user.password, password):
    token = jwt.encode(
      {'username': user.username, 'email':user.email, 'location': user.location, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
      app.config['SECRET_KEY'], "HS256")
    return jsonify({'token': token, 'email': user.email, 'username': user.username, 'location': user.location})
  return 'user or password incorrect', 401


if __name__ == '__main__':
  with app.app_context():

    # create inital database
    db.create_all()

    # add default admin user if not exists
    if User.query.filter_by(email=os.getenv('CABL_ADMIN_EMAIL', default='admin@email.de')).first() is None:
      user = User(
        username="Administrator",
        email=os.getenv('CABL_ADMIN_EMAIL', default='admin@email.de'),
        password=generate_password_hash (os.getenv('CABL_ADMIN_PASSWORD', default='admin'), method='sha256')
      )
      db.session.add(user)
      db.session.commit()

    # add default admin user if not exists
    if Location.query.filter_by(name=os.getenv('CABL_DEFAULT_LOCATION', default='Leipzig')).first() is None:
      location = Location(
        name=os.getenv('CABL_DEFAULT_LOCATION', default='Leipzig'),
      )
      db.session.add(location)
      db.session.commit()


  app.run(debug=True, host="0.0.0.0")