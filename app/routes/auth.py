from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            flash("All fields are required.")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Password do not match.")
            return redirect (url_for("auth.register"))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("auth.register"))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already exists.")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful.Please login.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username

            flash("Login successful.")
            return redirect(url_for("main.home"))

        flash("Invalid username or password.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))