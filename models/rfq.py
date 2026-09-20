from datetime import datetime
from extensions import db

class RFQ(db.Model):
    __tablename__ = "rfqs"

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery_location = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum("open", "closed"), default="open", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quotations = db.relationship(
        "Quotation",
        backref="rfq",
        lazy=True,
        cascade="all, delete-orphan"
    )
