from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Optional,
)


class ProductForm(FlaskForm):
    product_name = StringField(
        "Product name", validators=[DataRequired(), Length(max=120)]
    )
    price = DecimalField(
        "Price", places=2, validators=[InputRequired(), NumberRange(min=0)]
    )
    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=5000)]
    )
    stock_amount = IntegerField(
        "Stock amount", validators=[InputRequired(), NumberRange(min=0)]
    )
    submit = SubmitField()
