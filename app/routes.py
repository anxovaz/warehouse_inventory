from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy import select

from app import db
from app.forms import ProductForm
from app.models import Product

bp = Blueprint("inventory", __name__)


@bp.get("/")
def index():
    products = db.session.scalars(
        select(Product).order_by(Product.product_name, Product.id)
    ).all()
    return render_template("index.html", products=products)


@bp.route("/products/new", methods=["GET", "POST"])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            product_name=form.product_name.data.strip(),
            price=form.price.data,
            description=(form.description.data or "").strip(),
            stock_amount=form.stock_amount.data,
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added to inventory.", "success")
        return redirect(url_for("inventory.index"))
    return render_template("product_form.html", form=form, page_title="Add product")


@bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = db.get_or_404(Product, product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.product_name = form.product_name.data.strip()
        product.price = form.price.data
        product.description = (form.description.data or "").strip()
        product.stock_amount = form.stock_amount.data
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("inventory.index"))
    return render_template(
        "product_form.html", form=form, page_title="Edit product"
    )


@bp.post("/products/<int:product_id>/delete")
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product removed from inventory.", "success")
    return redirect(url_for("inventory.index"))
