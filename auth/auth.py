from flask import Blueprint,request,jsonify
from marshmallow import Schema,fields
from extensions import db
from models import User
from flask_jwt_extended import create_access_token



auth_bp=Blueprint("auth",__name__)

class UserIn(Schema):
    email = fields.Email(required=True,data_key="email")
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True,data_key="password")

@auth_bp.route("signup",methods=["POST"])
def signup():
    data=request.get_json()
    if not data or not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error":"Missing fields"}),400
    
    UserIn().load(data)

    if User.query.filter((User.username==data["username"])|(User.email==data["email"])).first():
        return jsonify({"error":"User already exists"}),400
    
    new_user=User(username=data["username"],email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()),201


@auth_bp.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    user =User.query.filter_by(username=data.get("username")).first()

    if user and user.check_password(data.get("password")):
        token=create_access_token(identity=str(user.id))
        return jsonify({"access_token":token}),200

    return jsonify({"error":"Invalid credentials"}),401