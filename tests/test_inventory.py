import pytest

from app import create_app, db
from app.models import Product


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "WTF_CSRF_ENABLED": False,
        }
    )
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_inventory_page_shows_empty_state(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Your inventory is empty" in response.data


def test_create_product(client, app):
    response = client.post(
        "/products/new",
        data={
            "product_name": "Packing tape",
            "price": "4.50",
            "description": "Clear tape",
            "stock_amount": "12",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Packing tape" in response.data
    with app.app_context():
        product = db.session.query(Product).one()
        assert product.price == 4.5
        assert product.stock_amount == 12


def test_product_validation_rejects_negative_stock(client):
    response = client.post(
        "/products/new",
        data={
            "product_name": "Packing tape",
            "price": "4.50",
            "description": "",
            "stock_amount": "-1",
        },
    )

    assert response.status_code == 200
    assert b"Number must be at least 0" in response.data


def test_edit_and_delete_product(client, app):
    with app.app_context():
        product = Product(
            product_name="Packing tape",
            price=4.50,
            description="Clear tape",
            stock_amount=12,
        )
        db.session.add(product)
        db.session.commit()
        product_id = product.id

    edit_response = client.post(
        f"/products/{product_id}/edit",
        data={
            "product_name": "Shipping tape",
            "price": "5.00",
            "description": "Heavy-duty clear tape",
            "stock_amount": "8",
        },
        follow_redirects=True,
    )
    assert edit_response.status_code == 200
    assert b"Shipping tape" in edit_response.data

    delete_response = client.post(
        f"/products/{product_id}/delete", follow_redirects=True
    )
    assert delete_response.status_code == 200
    assert b"Your inventory is empty" in delete_response.data
