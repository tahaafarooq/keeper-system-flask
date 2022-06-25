from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "/var/www/html/notes/uploaded"


@app.route("/")
def index():
    return jsonify({"RESP": "KEEPER SYSTEM FLASK"})


@app.route("/routes", methods=["GET"])
def routes():
    routes = {
        "route_register": "/register",
        "route_login": "/login",
        "route_forget_password": "/fpassword",
        "route_update_password": "/update",
        "route_upload_note": "/upload",
        "route_upload_note_remote": "/uploadremote",
        "route_fetch_note": "/fetch",
        "route_test_network": "/ping"
    }

    return jsonify(routes)


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        if len(username) > 3:
            if len(password) > 4 and password == cpassword:
                conn = sqlite3.connect("identifier.sqlite")
                curs = conn.cursor()
                curs.execute("INSERT INTO users (username, password) VALUES (?, ?)", f"({username}, {password})")
                conn.commit()
                conn.close()

                return jsonify({"RESP": "User Registered"})
            else:
                return jsonify({"RESP": "Password Doesn't Meet Requirement"})
        else:
            return jsonify({"RESP": "Username Should Be Length More Than 3 letters"})
    else:
        return jsonify({"RESP": "Method Not Allowed"})


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username != "" and password != "":
            conn = sqlite3.connect("identifier.sqlite")
            curs = conn.cursor()
            check = curs.execute(f"SELECT username FROM users WHERE username = '{username}' AND password = '{password}'").fetchall()
            conn.close()
            if len(check) == 0:
                return jsonify({"RESP": "User Does Not Exist"})
            else:
                return jsonify({"RESP": "Welcome"})
        else:
            return jsonify({"RESP": "No Input Provided"})
    else:
        return jsonify({"RESP": "Method Not Allowed"})


@app.route("/fpassword")
# will work on this function later
def forgot_password():
    return jsonify({"RESP": "Under Development"})


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        username = request.form.get("username")
        old_password = request.form.get("oldpass")
        new_password = request.form.get("newpass")
        if username != "":
            if old_password != new_password and len(new_password) > 4:
                conn = sqlite3.connect("identifier.sqlite")
                curs = conn.cursor()
                curs.execute(f"UPDATE users SET password = '{new_password}' WHERE username = '{username}'")
                conn.commit()
                conn.close()

                return jsonify({"RESP": "Profile Updated"})
            else:
                return jsonify({"RESP": "Passwords Needs To Be Unique"})
        else:
            return jsonify({"RESP": "Username Can't Be Blank"})
    else:
        return jsonify({"RESP": "Method Not Allowed"})


@app.route("/upload", methods=["POST"])
def upload_local():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"RESP": "No File Part In Request"})
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"RESP": "No Note Selected"})
        elif file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"RESP": "Note Uploaded Successfully"})
    else:
        return jsonify({"RESP": "Method Not Allowed"})


@app.route("/uploadremote", methods=["POST"])
def upload_remote():
    if request.method == "POST":
        link = request.form.get("link")
        if link != "" and len(link) > 8:
            try:
                import requests

                req = requests.get(link, allow_redirects=True)
                open("note", "wb").write(req.content)

                return jsonify({"RESP": "Note Uploaded Successfully"})
            except:
                return jsonify({"RESP": "Unable To Upload"})
        else:
            return jsonify({"RESP": "Link Not Correct"})
    else:
        return jsonify({"RESP": "Method Not Allowed"})


@app.route("/fetch", methods=["GET"])
def fetch():
    return jsonify({"RESP": "Under Development"})


@app.route("/ping", methods=["POST"])
def ping():
    if request.method == "POST":
        ip = request.form.get("ip")
        if len(ip) == 11 or len(ip) == 10:
            check = os.system(f"ping -c 2 {ip}")

            if check == 0:
                return jsonify({"RESP": "IP Is Up"})
            else:
                return jsonify({"RESP": "IP Is Down"})
        else:
            return jsonify({"RESP": ""})
    else:
        return jsonify({"RESP": "Method Not Allowed"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
