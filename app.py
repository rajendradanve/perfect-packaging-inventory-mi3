import os
from flask import (
    Flask, flash, render_template,  
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DB_NAME"]= os.environ.get("MONGO_DB_NAME")
app.config["MONGO_URI"]= os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
    
        if existing_user:
            # Check if password provided by existing user is correct
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                if session["user"] == "admin":
                    return redirect(url_for(
                        "admin", username=session["user"]))
                else:
                    return redirect(url_for(
                        "customer", username=session["user"]))
            else:
                # invalid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port =int(os.environ.get("PORT")),
        debug =True)



