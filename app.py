from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
import datetime

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        # flash("User %s is logged in"%session['actual_username'])
        username = session['actual_username']
        return redirect(url_for("show_newsfeed"))
    else:
        return render_template("index.html")

@app.route("/feed")
def show_newsfeed():
    rows = model.get_last_five_posts()
    return render_template("newsfeed.html", wall_posts = rows)

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    auth_user = model.authenticate(username, password)
    if auth_user != None:
        session['username'] = auth_user
        session['actual_username'] = username
    else:
        flash("Password incorrect, please try again!")

    return redirect(url_for("index"))

@app.route("/user/<username>", methods=["GET"])
def view_user(username):
    user_id = model.get_user_by_name(username)
    wall_posts = model.get_wall_posts(user_id)
    return render_template("wall.html", wall_posts = wall_posts, session_id = session['username'], username = username, profile_owner = session['actual_username'])

@app.route("/user/<username>/post", methods=["POST"])
def post_to_wall(username):
    id_from_users = model.get_user_by_name(username)
    author_id_from_users = session['username']
    date_time = str(datetime.datetime.now())
    post = request.form.get("post")
    model.post_to_wall(id_from_users, author_id_from_users, date_time, post)
    return redirect("/user/%s"%username)    
    # return render_template("test.html", a=id_from_users, b=author_id_from_users, c=date_time, d=post)


@app.route("/register", methods=["GET"])
def register():
    if session.get('username'):
        real_name = session.get('actual_username')
        return redirect("/user/%s"%real_name)
    else:
        return render_template("register.html")

@app.route("/register/create_account", methods=["POST"])
def create_account():
    if session.get('username'):
        real_name = session.get('actual_username')
        return redirect("/user/%s"%real_name)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if model.get_user_by_name(username) == "Nope":
            model.register_new_user(username, password)
            flash("Account created!")
            return redirect(url_for("process_login"))
        else:
            flash("You already exist!")
            return redirect(url_for("register"))

@app.route("/search", methods=["POST"])
def search_user():
    username_to_search = request.form.get("search")
    model.get_user_by_name(username_to_search)
    if model.get_user_by_name(username_to_search) == "Nope":
            flash("User not found")
            return redirect(request.referrer)
    else:
        return redirect("/user/%s"%username_to_search)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/game")
def game():
    return render_template("game.html")


if __name__ == "__main__":
    app.run(debug = True)



