from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
import datetime

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
        session['actual_username'] = username
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))

@app.route("/user/<username>", methods=["GET"])
def view_user(username):
    user_id = model.get_user_by_name(username)
    wall_posts = model.get_wall_posts(user_id)
    return render_template("wall.html", wall_posts = wall_posts, session_id = session['username'], username = username)

@app.route("/user/<username>/post", methods=["POST"])
def post_to_wall(username):
    id_from_users = model.get_user_by_name(username)
    author_id_from_users = session['username']
    date_time = str(datetime.datetime.now())
    post = request.form.get("post")
    model.post_to_wall(id_from_users, author_id_from_users, date_time, post)
    return redirect("/user/%s"%username)    
    # return render_template("test.html", a=id_from_users, b=author_id_from_users, c=date_time, d=post)


@app.route("/register")
def register():
    if session.get('username'):
        real_name = session.get('actual_username')
        return redirect("/user/%s"%real_name)
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)



