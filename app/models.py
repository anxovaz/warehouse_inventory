from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column("productName", db.String(120), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    stock_amount = db.Column("stockAmount", db.Integer, nullable=False, default=0)
