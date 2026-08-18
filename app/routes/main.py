from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("home.html")