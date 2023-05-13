from app import app
from model.UserModel import UserModel
from flask import request
import traceback

obj = UserModel()

@app.route("/login", methods=["POST"])
def login():
    return obj.login(request.json)

@app.route("/signup", methods=["POST"])
def signup():
    return obj.signup(request.json)

@app.route("/update", methods=["PUT"])
def update():
    return obj.update(request.json)

@app.route("/delete/<uname>", methods=["DELETE"])
def delete(uname):
    return obj.delete(uname)

@app.route("/logout/<uname>", methods=["PUT"])
def logout(uname):
    return obj.logout(uname)

@app.route("/block/<uname>", methods=["PUT"])
def block(uname):
    return obj.block(uname)
