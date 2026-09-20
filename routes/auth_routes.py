from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from models.user import User
from extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        if not name or not email or not password or role not in ("buyer", "supplier"):
            flash("All fields are required and role must be selected.", "danger")
            return render_template("register.html")

        if len(name) < 2:
            flash("Name must contain at least 2 characters.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
            return render_template("register.html")

        if "@" not in email or "." not in email.split("@")[-1]:
            flash("Please enter a valid email address.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return redirect(url_for("auth.login"))

        user = User(name=name, email=email, role=role)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Email is already registered.", "danger")
            return render_template("register.html")

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role
        session["user_name"] = user.name

        if user.role == "buyer":
            return redirect(url_for("buyer.dashboard"))
        return redirect(url_for("supplier.dashboard"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
