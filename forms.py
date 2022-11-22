from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField


class AddClientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class CreateProductForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
