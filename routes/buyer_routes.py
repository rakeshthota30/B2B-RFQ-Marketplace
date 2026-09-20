from datetime import date
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.rfq import RFQ
from models.quotation import Quotation
from extensions import db

buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")

def buyer_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("role") != "buyer":
            flash("Buyer access is required.", "danger")
            return redirect(url_for("supplier.dashboard"))
        return route_function(*args, **kwargs)
    return wrapper

def parse_rfq_form():
    product_name = request.form.get("product_name", "").strip()
    description = request.form.get("description", "").strip()
    quantity_text = request.form.get("quantity", "").strip()
    delivery_location = request.form.get("delivery_location", "").strip()
    deadline_text = request.form.get("deadline", "").strip()

    if not all([product_name, description, quantity_text, delivery_location, deadline_text]):
        return None, "All fields are required."

    try:
        quantity = int(quantity_text)
        if quantity <= 0:
            return None, "Quantity must be greater than zero."
    except ValueError:
        return None, "Quantity must be a valid whole number."

    try:
        deadline = date.fromisoformat(deadline_text)
    except ValueError:
        return None, "Invalid deadline."

    if deadline < date.today():
        return None, "Deadline cannot be in the past."

    return {
        "product_name": product_name,
        "description": description,
        "quantity": quantity,
        "delivery_location": delivery_location,
        "deadline": deadline,
    }, None

@buyer_bp.route("/dashboard")
@buyer_required
def dashboard():
    rfqs = RFQ.query.filter_by(buyer_id=session["user_id"]).order_by(RFQ.created_at.desc()).all()
    return render_template("buyer/dashboard.html", rfqs=rfqs)

@buyer_bp.route("/rfq/create", methods=["GET", "POST"])
@buyer_required
def create_rfq():
    if request.method == "POST":
        data, error = parse_rfq_form()

        if error:
            flash(error, "danger")
            return render_template("buyer/create_rfq.html")

        rfq = RFQ(buyer_id=session["user_id"], **data)
        db.session.add(rfq)
        db.session.commit()

        flash("RFQ created successfully.", "success")
        return redirect(url_for("buyer.dashboard"))

    return render_template("buyer/create_rfq.html")

@buyer_bp.route("/rfq/<int:rfq_id>/edit", methods=["GET", "POST"])
@buyer_required
def edit_rfq(rfq_id):
    rfq = RFQ.query.filter_by(id=rfq_id, buyer_id=session["user_id"]).first_or_404()

    if request.method == "POST":
        data, error = parse_rfq_form()

        if error:
            flash(error, "danger")
            return render_template("buyer/edit_rfq.html", rfq=rfq)

        rfq.product_name = data["product_name"]
        rfq.description = data["description"]
        rfq.quantity = data["quantity"]
        rfq.delivery_location = data["delivery_location"]
        rfq.deadline = data["deadline"]

        db.session.commit()
        flash("RFQ updated successfully.", "success")
        return redirect(url_for("buyer.dashboard"))

    return render_template("buyer/edit_rfq.html", rfq=rfq)

@buyer_bp.route("/rfq/<int:rfq_id>/delete", methods=["POST"])
@buyer_required
def delete_rfq(rfq_id):
    rfq = RFQ.query.filter_by(id=rfq_id, buyer_id=session["user_id"]).first_or_404()
    db.session.delete(rfq)
    db.session.commit()

    flash("RFQ deleted successfully.", "success")
    return redirect(url_for("buyer.dashboard"))

@buyer_bp.route("/rfq/<int:rfq_id>")
@buyer_required
def rfq_details(rfq_id):
    rfq = RFQ.query.filter_by(id=rfq_id, buyer_id=session["user_id"]).first_or_404()
    return render_template("buyer/rfq_details.html", rfq=rfq)

@buyer_bp.route("/rfq/<int:rfq_id>/quotations")
@buyer_required
def quotations(rfq_id):
    rfq = RFQ.query.filter_by(id=rfq_id, buyer_id=session["user_id"]).first_or_404()
    quotations = Quotation.query.filter_by(rfq_id=rfq.id).order_by(Quotation.created_at.desc()).all()
    return render_template(
        "buyer/quotations.html",
        rfq=rfq,
        quotations=quotations
    )
