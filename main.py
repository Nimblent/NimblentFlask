from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    session,
    redirect,
    url_for,
    flash,
)
from db import School, Students, Teachers
import hashlib


app = Flask("NimblentFLASK")
app.config["SECRET_KEY"] = "nimblent"
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_SAMESITE="None")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if School.select().count() == 0:
            schoolname = str(request.form["schoolname"])
            rne = str(request.form["username"])
            password = hashlib.sha256(
                request.form["password"].encode("utf-8")
            ).hexdigest()
            verifpwd = hashlib.sha256(
                request.form["passwordconf"].encode("utf-8")
            ).hexdigest()
            if password == verifpwd:
                School(schoolName=schoolname, rne=rne, password=password)
                print("Etablissement initialisé!")
                return render_template("login.html", type=2)
            else:
                return render_template("login.html", type=0)
        else:
            username = str(request.form["username"])
            password = hashlib.sha256(
                request.form["password"].encode("utf-8")
            ).hexdigest()
            dbpassword = School.selectBy(rne=username)
            if dbpassword.count() < 1:
                dbpassword = Students.selectBy(username=username) if Students.selectBy(username=username).count() >= 1 else Teachers.selectBy(username=username)
                account_type = "student" if Students.selectBy(username=username).count() >= 1 else "teacher"
                print(dbpassword)
                if dbpassword.count() < 1:
                    flash("Indentifiants invalides", "error")
                    return render_template("login.html", type=1, username=username)
                elif dbpassword[0].toDict()["password"] == password:
                    session["account_type"] = account_type
                    session["username"] = username
                    session["password"] = dbpassword[0].toDict()["password"]
                    flash(f"Connecté en tant que {dbpassword[0].toDict()['firstName']} {dbpassword[0].toDict()['lastName']} !", "success")
                    print(session.get("account_type"))
                    return render_template("student.html", School=School) if account_type == "student" else render_template("teacher.html", School=School)   
                else:
                    flash("Indentifiants invalides", "error")
                    return render_template("login.html", type=1,username=username)

            if dbpassword[0].toDict()["password"] == password:
                session["account_type"] = "admin"
                session["rne"] = username
                session["password"] = dbpassword[0].toDict()["password"]
                flash("Connecté !", "success")
                return redirect(url_for("admin"))

            flash("Indentifiants invalides", "error")
            return render_template("login.html", type=1, username=username)
    else:
        if School.select().count() == 0:
            return render_template("login.html", type=0)
        else:
            if session.get("account_type") and session["account_type"] == "student" and session.get("username"):
                return render_template("student.html", School=School)
            elif session.get("account_type") and session["account_type"] == "teacher" and session.get("username"):
                return render_template("teacher.html", School=School)
            return render_template("login.html", type=1)


@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if School.select().count() == 0:
        return redirect(url_for("index"))
    else:
        if request.method == "POST":
            rne = str(request.form["username"])
            password = hashlib.sha256(
                request.form["password"].encode("utf-8")
            ).hexdigest()
            dbpassword = School.selectBy(rne=rne)
            if dbpassword.count() < 1:
                flash("Indentifiants invalides", "error")
                return render_template("login.html", type=2, username=rne)

            if dbpassword[0].toDict()["password"] == password:
                session["account_type"] = "admin"
                session["rne"] = rne
                session["password"] = dbpassword[0].toDict()["password"]
                flash("Connecté !", "success")
                print(session.get("account_type"))
                return render_template("panel.html", School=School)

            flash("Indentifiants invalides", "error")
            return render_template("login.html", type=2,username=rne)
        else:
            print(session.get("account_type"))
            if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
                return render_template("panel.html", School=School, Students=Students, Teachers=Teachers)
            return render_template("login.html", type=2)

@app.route("/admin/addstudent/", methods=["GET", "POST"])
def add_student():
    if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
        if request.method == "POST":
            if Students.selectBy(username=request.form["username"]).count() < 1 and Teachers.selectBy(username=request.form["username"]).count() < 1:
                Students(username=request.form["username"], firstName=request.form["firstName"], lastName=request.form["lastName"], level=request.form["level"], password=hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest())
                flash("Utilisateur.rice créé.e !", "success")
                return redirect(url_for("admin"))
            else:
                flash("Utilisateur.rice déjà existant.e !", "warning")
                return render_template("login.html", type=3)
        else:
            return render_template("login.html", type=3)
    else:
        return redirect(url_for("index"))

@app.route("/admin/addteacher/", methods=["GET", "POST"])
def add_teacher():
    if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
        if request.method == "POST":
            if Students.selectBy(username=request.form["username"]).count() < 1 and Teachers.selectBy(username=request.form["username"]).count() < 1:
                Teachers(username=request.form["username"], firstName=request.form["firstName"], lastName=request.form["lastName"], password=hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest())
                flash("Utilisateur.rice créé.e !", "success")
                return redirect(url_for("admin"))
            else:
                flash("Utilisateur.rice déjà existant.e !", "warning")
                return render_template("login.html", type=4)
        else:
            return render_template("login.html", type=4)
    else:
        return redirect(url_for("index"))


@app.route("/logout/", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization, TOKEN, token"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


app.run(port=8000, host="127.0.0.1", threaded=True, debug=True)
