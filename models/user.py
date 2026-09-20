from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("buyer", "supplier"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    rfqs = db.relationship("RFQ", backref="buyer", lazy=True, cascade="all, delete-orphan")
    quotations = db.relationship("Quotation", backref="supplier", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
