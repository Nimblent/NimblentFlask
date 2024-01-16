from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from db import School
import hashlib


app = Flask("NimblentFLASK")
app.config["SECRET_KEY"] = "nimblentdev"
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_SAMESITE="None")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if School.select().count() == 0:
            schoolname = str(request.form["schoolname"])
            ogeccode = str(request.form["username"])
            password = hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest()
            verifpwd = hashlib.sha256(request.form["passwordconf"].encode('utf-8')).hexdigest()
            if password == verifpwd:
                School(schoolName=schoolname, ogecCode=ogeccode, password=password)
                print('Etablissement initialisé!')
                return render_template("index.html", message=None, type=1)
            else:
                return render_template("index.html", message="Les mots de passe ne correspondent pas.", type=0)
    else:
        if School.select().count() == 0:
            return render_template("index.html", message=None, type=0)
        else:
            return render_template("index.html", message=None, type=1)

@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if School.select().count() == 0:
        return url_for("index")
    else:
        if request.method == 'POST':
            ogeccode = str(request.form["username"])
            password = hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest()
            dbpassword = School.selectBy(ogecCode=ogeccode)
            print(dbpassword)
            if dbpassword["password"] == password:
                pass
        else:
            return render_template("index.html", message=None, type=2)
        
@app.route('/admin/panel/', methods=['GET'])
def panel_admin():
    return render_template("index.html", message="Panel admin", type=2)

@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization, TOKEN, token"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


app.run(port=8000, host="0.0.0.0", threaded=True, debug=True)