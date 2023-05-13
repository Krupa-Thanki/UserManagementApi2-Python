import json
import socket
from datetime import datetime
import mysql.connector


class UserModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host='localhost', user='root', password='', database='userdetails')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)

            print('connection successful')
        except:
            print('some errors')



    def login(self, data):

        self.cur.execute(f"SELECT username, password FROM user where username = '{data['username']}' AND password = '{data['password']}'")
        result = self.cur.fetchall()

        self.cur.execute(f"UPDATE user SET isActive = 1 Where username = '{data['username']}'")

        # get date for log
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")

        # get ip for log
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        # data insert in log table
        username = data['username']
        self.cur.execute(
            "INSERT INTO userLog (logdate,ipaddress,id,activity) values ('" + dt + "','" + ip + "',(SELECT id FROM user WHERE username = '" + username + "'),'login')")

        if len(result) > 0:
            return "Login successful"
        else:
            return "no data found"



    def signup(self, data):
        # data insert in user table
        self.cur.execute("INSERT INTO user (username,password,email,isActive,isBlock) values ('" + data['username'] + "','" + data['password'] + "','" + data['email'] + "',0,0)")

        # get date for log
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")

        # get ip for log
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        # data insert in log table
        username = data['username']
        self.cur.execute("INSERT INTO userLog (logdate,ipaddress,id,activity) values ('" + dt + "','" + ip + "',(SELECT id FROM user WHERE username = '" + username + "'),'Register')")

        return "user created successfully"



    def delete(self, uname):
        self.cur.execute("DELETE FROM user WHERE id = (SELECT id FROM user WHERE username = '" + uname + "')")

        # get date for log
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")

        # get ip for log
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        # data insert in log table
        username = uname
        self.cur.execute(
            "INSERT INTO userLog (logdate,ipaddress,id,activity) values ('" + dt + "','" + ip + "',(SELECT id FROM user WHERE username = '" + username + "'),'Register')")

        return "user deleted"



    def update(self, data):
        result = ""
        username = data['username']
        newname = data['newname']
        newpwd = data['newpwd']

        if newname is not None:
            self.cur.execute(
                "UPDATE user SET username = '" + newname + "' WHERE id = (SELECT id FROM user WHERE username = '" + username + "')")
            result += " username updated"

        if newpwd is not None:
            self.cur.execute(
                "UPDATE user SET username = '" + newpwd + "' WHERE id = (SELECT id FROM user WHERE username = '" + username + "')")
            result += " password updated"

        return result



    def logout(self, uname):
        self.cur.execute("UPDATE user SET isActive = 0 Where username = '"+uname+"'")

        # get date for log
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")

        # get ip for log
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        # data insert in log table
        username = uname
        self.cur.execute(
            "INSERT INTO userLog (logdate,ipaddress,id,activity) values ('" + dt + "','" + ip + "',(SELECT id FROM user WHERE username = '" + uname + "'),'Logout')")

        return "user logged out"

    def block(self, uname):
        self.cur.execute("UPDATE user SET isBlock = 1 Where username = '"+uname+"'")

        # get date for log
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")

        # get ip for log
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        # data insert in log table
        username = uname
        self.cur.execute(
            "INSERT INTO userLog (logdate,ipaddress,id,activity) values ('" + dt + "','" + ip + "',(SELECT id FROM user WHERE username = '" + uname + "'),'blocked')")

        return "user Blocked"
