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
from db import School, User
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
                dbpassword = User.selectBy(username=username)
                if dbpassword.count() < 1:
                    flash("Indentifiants invalides", "error")
                    return render_template("login.html", type=1, username=username)
                elif dbpassword[0].password == password:
                    session["account_type"] = "teacher" if dbpassword[0].is_a_teacher else "student"
                    session["username"] = username
                    session["password"] = dbpassword[0].password
                    flash(f"Connecté en tant que {dbpassword[0].firstName} {dbpassword[0].lastName} !", "success")
                    # return render_template("userpanel.html", School=School)
                    return render_template("adminpanel.html", School=School, users=User)
                else:
                    flash("Indentifiants invalides", "error")
                    return render_template("login.html", type=1,username=username)

            if dbpassword[0].password == password:
                session["account_type"] = "admin"
                session["rne"] = username
                session["password"] = dbpassword[0].password
                flash("Connecté !", "success")
                return redirect(url_for("admin"))

            flash("Indentifiants invalides", "error")
            return render_template("login.html", type=1, username=username)
    else:
        if School.select().count() == 0:
            return render_template("login.html", type=0)
        else:
            if session.get("account_type") and session.get("username"):
                # return render_template("userpanel.html", School=School)
                return render_template("adminpanel.html", School=School, users=User)
            return render_template("login.html", type=1)


@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if School.select().count() == 0:
        return redirect(url_for("index"))
    else:
        if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
            return render_template("adminpanel.html", School=School, users=User)
        return redirect(url_for("index"))

@app.route("/admin/adduser/", methods=["GET", "POST"])
def add_user():
    if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
        if request.method == "POST":
            if User.selectBy(username=request.form["username"]).count() < 1:
                print(request.form.get("isATeacher"))
                User(
                    username=request.form["username"],
                    firstName=request.form["firstName"],
                    lastName=request.form["lastName"],
                    permissions=0,
                    password=hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest(),
                    is_a_teacher=request.form.get("isATeacher")=="on"
                )
                flash("Utilisateur.rice créé.e !", "success")
                return redirect(url_for("admin"))
            else:
                flash("Utilisateur.rice déjà existant.e !", "warning")
                return render_template("login.html", type=3)
        else:
            return render_template("login.html", type=3)
    else:
        return redirect(url_for("index"))

@app.route("/admin/schedule/create/", methods=["POST"])
def create_schedule():
    pass

@app.route("/admin/schedule/edit/", methods=["POST"])
def edit_schedule():
    pass

@app.route("/admin/schedule/remove/<id>", methods=["POST"])
def edit_schedule(id):
    pass


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
