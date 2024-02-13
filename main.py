import subprocess
# installation automatique des packages requis pour lancer le projet
packagesInstall = subprocess.run(["pip", "install", "--user", "-r", "requirements.txt"])

if packagesInstall.returncode != 0:
    print("Erreur lors de l'exécution de l'installation des packages.")

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
from db import School, User, Course
import hashlib


app = Flask("NimblentFLASK")
app.config["SECRET_KEY"] = "nimblent"
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_SAMESITE="None")


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Fonction qui gère la page d'accueil de l'application.
    
    Cette fonction vérifie si la méthode de la requête est "POST". Si c'est le cas, elle effectue différentes vérifications
    et actions en fonction de l'état de la base de données et des données envoyées par le formulaire.
    Si la méthode de la requête est "GET", elle vérifie si l'utilisateur est déjà connecté et renvoie la page d'accueil
    correspondante en fonction de son type de compte.
    
    Retourne:
            - Si la méthode de la requête est "POST" et les vérifications sont réussies, renvoie la page de connexion avec
                un message de succès.
            - Si la méthode de la requête est "POST" et les vérifications échouent, renvoie la page de connexion avec un
                message d'erreur correspondant.
            - Si la méthode de la requête est "GET" et l'utilisateur est déjà connecté, renvoie la page d'accueil correspondante.
            - Si la méthode de la requête est "GET" et aucun établissement n'est enregistré dans la base de données, renvoie
                la page de connexion avec un message indiquant qu'aucun établissement n'est enregistré.
            - Si la méthode de la requête est "GET" et aucun utilisateur n'est connecté, renvoie la page de connexion.
    """

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
    """
    Fonction qui gère l'accès à la page d'administration.

    Vérifie si une école est enregistrée dans la base de données.
    Si aucune école n'est enregistrée, redirige vers la page d'accueil.
    Sinon, vérifie si l'utilisateur est connecté en tant qu'administrateur
    et si le RNE (Répertoire National des Établissements) de l'utilisateur
    correspond au RNE de l'école enregistrée.
    Si les conditions sont remplies, affiche le panneau d'administration.
    Sinon, redirige vers la page d'accueil.
    """

    if School.select().count() == 0:
        return redirect(url_for("index"))
    else:
        if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
            return render_template("adminpanel.html", School=School, users=User)
        return redirect(url_for("index"))

@app.route("/admin/adduser/", methods=["GET", "POST"])
def add_user():
    """
    Ajoute un nouvel utilisateur en base de données.

    Cette fonction vérifie si l'utilisateur est un administrateur et possède le bon RNE (Numéro d'Enregistrement pour l'Éducation) de l'école.
    Si la méthode de requête est POST, elle vérifie si le nom d'utilisateur est unique et crée un nouvel utilisateur avec les informations fournies.
    Le mot de passe est haché en utilisant l'algorithme SHA256 avant d'être stocké dans la base de données.
    Si le nom d'utilisateur existe déjà, un message d'avertissement est affiché.
    Si la méthode de requête n'est pas POST, la page de connexion est rendue.
    Si l'utilisateur n'est pas un administrateur ou a le mauvais RNE de l'école, il est redirigé vers la page d'accueil.

    Retourne:
        - Si l'utilisateur est ajouté avec succès, il est redirigé vers la page d'administration.
        - Si le nom d'utilisateur existe déjà, la page de connexion est rendue avec un message d'avertissement.
        - Si l'utilisateur n'est pas un administrateur ou a le mauvais RNE de l'école, il est redirigé vers la page d'accueil.
    """

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

@app.route("/admin/schedule/create/", methods=["GET", "POST"])
def create_schedule():
    """
    Crée un emploi du temps.

    Vérifie si l'utilisateur est connecté en tant qu'administrateur et si le compte est associé à l'établissement scolaire.
    Si la méthode de requête est POST, crée un nouveau cours avec les informations fournies dans le formulaire.
    Sinon, affiche le formulaire pour créer un emploi du temps.
    Si l'utilisateur n'est pas connecté en tant qu'administrateur ou si le compte n'est pas associé à l'établissement scolaire, redirige vers la page d'accueil.

    Retourne:
        - Redirection vers la page d'accueil si l'utilisateur n'est pas connecté en tant qu'administrateur ou si le compte n'est pas associé à l'établissement scolaire.
        - Redirection vers la page d'administration si le cours est créé avec succès.
    """
    
    if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
        if request.method == "POST":
            Course(
                start=request.form["start"],
                end=request.form["end"],
                professor=request.form["professors"],
                groups=request.form["groups"],
                subject=request.form["subject"],
                room=request.form["room"],
            )
            flash(f"Cours ajouté !", "success")
            return redirect(url_for("admin"))
        else:
            return render_template("schedule.html", type=0, users=User)
    else:
        return redirect(url_for("index"))

@app.route("/admin/schedule/edit/<id>", methods=["GET", "POST"])
def edit_schedule():
    """
    Fonction qui permet de modifier l'emploi du temps.

    Vérifie d'abord si l'utilisateur est connecté en tant qu'administrateur et si le numéro RNE de l'école correspond à celui enregistré dans la session.
    Si les conditions sont remplies, renvoie le template "schedule.html" avec le type 1.
    Sinon, redirige vers la page d'accueil.
    """
    if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
        return render_template("schedule.html", type=1)
    else:
        return redirect(url_for("index"))

@app.route("/admin/schedule/remove/<id>/", methods=["GET"])
def delete_schedule(id):
    """
    Supprime un emploi du temps en fonction de son identifiant.

    Args:
        id (int): L'identifiant de l'emploi du temps à supprimer.

    Retpurne:
        Une redirection vers la page "admin" si l'utilisateur est un administrateur et a le bon RNE, sinon une redirection vers la page "index".
    """
    if session.get("account_type") and session["account_type"] == "admin" and session.get("rne") and session["rne"] == School.select().getOne().rne:
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("index"))


@app.route("/logout/", methods=["GET"])
def logout():
    """
    Déconnecte l'utilisateur en effaçant la session en cours.
    Redirige vers la page d'accueil.
    """
    session.clear()
    return redirect(url_for("index"))


@app.after_request
def add_header(response):
    """
    Ajoute les en-têtes nécessaires à la réponse HTTP pour autoriser les requêtes cross-origin (CORS).
    
    Args:
        response (flask.Response): La réponse HTTP à laquelle ajouter les en-têtes.

    Retourne:
        La réponse HTTP avec les en-têtes ajoutés.
    """
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization, TOKEN, token"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


app.run(port=8000, host="127.0.0.1", threaded=True, debug=True)
