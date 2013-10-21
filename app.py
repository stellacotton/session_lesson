from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        flash("User %s is logged in"%session['username'])
        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    auth_user = model.authenticate(username, password)
    if auth_user != None:
        flash("User authenticated!")
        session['username'] = auth_user
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))

@app.route("/user/<username>", methods=["GET"])
def view_user(username):
    user_id = model.get_user_by_name(username)
    wall_posts = model.get_wall_posts(user_id)
    return render_template("wall.html", wall_posts = wall_posts, session_id = session['username'])

@app.route("user/<username>/post", methods=["POST"])
def post_to_wall(username):
    id_from_users = model.get_user_by_name(username)
    author_id_from_users = session["username"]








@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)



