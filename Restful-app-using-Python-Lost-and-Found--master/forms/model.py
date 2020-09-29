# model.py
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators, DateField, SelectField
from flask_wtf import Form
from datetime import date


class RegForm(Form):
    username = StringField('Username', [validators.DataRequired(message="Username exist. Choose another")])
    password = PasswordField('New Password', [validators.DataRequired(),
                                              validators.Regexp("^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{8,}$",
                                                                message="Password should be minimum 8 characters with atleast 1 alphabet, 1 number and 1 special character"),
                                              validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')


class SearchForm(Form):
    search_string = StringField('Search')
    submit = SubmitField('Search')


class InsertForm(Form):
    name = StringField('Product Name', [validators.DataRequired(message="Required field")])
    description = StringField('Product Description', [validators.DataRequired(message="Required field")])
    location = StringField('Product Location', [validators.DataRequired()])
    Date = DateField('Date Found', default=date.today, format='%d-%m-%Y',
                     validators=[validators.DataRequired(message="Date format day-month-year (10-12-2020)")])
    status = SelectField('Product Status',
                         choices=[('unclaimed', 'un-claimed'), ('Donate', 'Donate'), ('Claimed', 'Claimed')])
    submit = SubmitField('Submit', [validators.DataRequired()])
