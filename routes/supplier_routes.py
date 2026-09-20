from datetime import date
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from models.rfq import RFQ
from models.quotation import Quotation
from extensions import db

supplier_bp = Blueprint("supplier", __name__, url_prefix="/supplier")

def supplier_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("role") != "supplier":
            flash("Supplier access is required.", "danger")
            return redirect(url_for("buyer.dashboard"))
        return route_function(*args, **kwargs)
    return wrapper

@supplier_bp.route("/dashboard")
@supplier_required
def dashboard():
    search = request.args.get("search", "").strip()
    location = request.args.get("location", "").strip()

    query = RFQ.query.filter(
        RFQ.status == "open",
        RFQ.deadline >= date.today()
    )

    if search:
        query = query.filter(
            or_(
                RFQ.product_name.ilike(f"%{search}%"),
                RFQ.description.ilike(f"%{search}%")
            )
        )

    if location:
        query = query.filter(RFQ.delivery_location.ilike(f"%{location}%"))

    rfqs = query.order_by(RFQ.deadline.asc()).all()

    locations = [
        row[0] for row in
        db.session.query(RFQ.delivery_location)
        .filter(RFQ.status == "open")
        .distinct()
        .order_by(RFQ.delivery_location.asc())
        .all()
    ]

    return render_template(
        "supplier/dashboard.html",
        rfqs=rfqs,
        search=search,
        location=location,
        locations=locations
    )

@supplier_bp.route("/rfq/<int:rfq_id>")
@supplier_required
def rfq_details(rfq_id):
    rfq = RFQ.query.filter_by(id=rfq_id, status="open").first_or_404()
    existing_quote = Quotation.query.filter_by(
        rfq_id=rfq.id,
        supplier_id=session["user_id"]
    ).first()

    return render_template(
        "supplier/rfq_details.html",
        rfq=rfq,
        existing_quote=existing_quote
    )

@supplier_bp.route("/rfq/<int:rfq_id>/quote", methods=["POST"])
@supplier_required
def submit_quote(rfq_id):
    rfq = RFQ.query.filter_by(id=rfq_id, status="open").first_or_404()

    if rfq.deadline < date.today():
        flash("This RFQ deadline has passed.", "danger")
        return redirect(url_for("supplier.dashboard"))

    if Quotation.query.filter_by(
        rfq_id=rfq.id,
        supplier_id=session["user_id"]
    ).first():
        flash("You have already submitted a quotation for this RFQ.", "warning")
        return redirect(url_for("supplier.rfq_details", rfq_id=rfq.id))

    price_text = request.form.get("quoted_price", "").strip()
    delivery_time = request.form.get("delivery_time", "").strip()
    message = request.form.get("message", "").strip()

    if not price_text or not delivery_time:
        flash("Quoted price and delivery time are required.", "danger")
        return redirect(url_for("supplier.rfq_details", rfq_id=rfq.id))

    try:
        price = float(price_text)
        if price <= 0:
            raise ValueError
    except ValueError:
        flash("Quoted price must be a valid number greater than zero.", "danger")
        return redirect(url_for("supplier.rfq_details", rfq_id=rfq.id))

    quotation = Quotation(
        rfq_id=rfq.id,
        supplier_id=session["user_id"],
        quoted_price=price,
        delivery_time=delivery_time,
        message=message
    )

    try:
        db.session.add(quotation)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("A quotation from you already exists for this RFQ.", "warning")
        return redirect(url_for("supplier.rfq_details", rfq_id=rfq.id))

    flash("Quotation submitted successfully.", "success")
    return redirect(url_for("supplier.my_quotations"))

@supplier_bp.route("/quotations")
@supplier_required
def my_quotations():
    quotations = Quotation.query.filter_by(
        supplier_id=session["user_id"]
    ).order_by(Quotation.created_at.desc()).all()

    return render_template(
        "supplier/my_quotations.html",
        quotations=quotations
    )
