from dataclasses import Field

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange, ValidationError, Optional

app = Flask(__name__)
finance = {}


def comment_correctness(max: int):
    def _comment_correctness(form: FlaskForm, field: Field):
        len_comment = len(str(field.data))
        if len_comment > max:
            raise ValidationError(f"The comment size should not exceed {max} characters")

    return _comment_correctness


def symbol_correctness():
    def _name_correctness(form: FlaskForm, field: Field):
        name = str(field.data[0])
        if name.islower():
            raise ValidationError(f"Must begin with a capital letter")

    return _name_correctness


def index_positive():
    def _nindex_positive(form: FlaskForm, field: Field):
        index = int(field.data)
        if index < 0:
            raise ValidationError(f"The index must be greater than -1")

    return _nindex_positive


def number_length(min: int, max: int):
    def _number_length(form: FlaskForm, field: Field):
        len_number = len(str(field.data))
        if len_number < min or len_number > max:
            raise ValidationError(f"The number length is entered incorrect: {len_number}"
                                  f" The allowed number length is from {min} to {max} characters")

    return _number_length


class NumberLength:
    def __call__(self, form: FlaskForm, field: Field):
        len_number = len(str(field.data))
        if len_number < 10 or len_number > 10:
            raise ValidationError(f"The number length is entered incorrect: {len_number}"
                                  f" The allowed number length is from {10} to {10} characters")


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), number_length(10, 10)])
    name = StringField(validators=[InputRequired(), symbol_correctness()])
    address = StringField(validators=[InputRequired(), symbol_correctness()])
    index = IntegerField(validators=[InputRequired(), index_positive()])
    comment = StringField(validators=[comment_correctness(20)])


@app.route('/registration', methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)