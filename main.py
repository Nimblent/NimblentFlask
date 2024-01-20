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
from db import School
import hashlib


app = Flask("NimblentFLASK")
app.config["SECRET_KEY"] = "nimblentdev"
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
                return render_template("login.html", message=None, type=2)
            else:
                return render_template("login.html", type=0)
        else:
            return redirect(url_for("index"))
    else:
        if School.select().count() == 0:
            return render_template("login.html", message=None, type=0)
        else:
            return render_template("login.html", message=None, type=1)


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
                return render_template("login.html", type=2, rne=rne)

            if dbpassword[0].toDict()["password"] == password:
                session["account_type"] = "admin"
                session["rne"] = rne
                session["password"] = dbpassword[0].toDict()["password"]
                flash("Connecté !", "success")
                return render_template("panel.html", School=School)

            flash("Indentifiants invalides", "error")
            return render_template("login.html", type=2)
        else:
            if (
                session.get("account_type")
                and session["account_type"] == "admin"
                and session.get("rne")
                and session["rne"] == School.select().getOne().rne
            ):
                return render_template("panel.html", School=School)
            return render_template("login.html", message=None, type=2)


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


app.run(port=8000, host="0.0.0.0", threaded=True, debug=True)
