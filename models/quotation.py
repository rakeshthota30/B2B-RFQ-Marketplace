from datetime import datetime
from extensions import db

class Quotation(db.Model):
    __tablename__ = "quotations"

    id = db.Column(db.Integer, primary_key=True)
    rfq_id = db.Column(db.Integer, db.ForeignKey("rfqs.id", ondelete="CASCADE"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quoted_price = db.Column(db.Numeric(12, 2), nullable=False)
    delivery_time = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("rfq_id", "supplier_id", name="unique_supplier_rfq"),
    )
