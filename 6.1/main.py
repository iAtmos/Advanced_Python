import logging
from flask import Flask
from flask_wtf import flaskForm
from wtforms import InteqerField
from wtforms.validators import InputRequired


app = Flask(__name__)
logger = logging.getLogger('fd')


class DivideForm(FlaskForm):
    a = InteqerField(validators=[InputRequired])
    b = InteqerField(validators=[InputRequired])


@app.route('/devide/', methods=["GET"])
def divide():
    form = DivideForm()

    if form.validate_on_submite():
        a, b = form.a.data, form.b.data
        logger.debug(f"Form is valid. a={a}, b={b}")
        return f"a / b = {a / b:.2}"
    logger.error(f"Form is not valid, error={form.errors}")
    return f"Bad reqwest", 400


@app.errorhandler(ZeroDivisionError)
def handle_exception(e: ZeroDivisionError):
    logger.exception("We are unable to divide by zero!", exc_info=e)
    return "We are unable to divide by zero!", 400


if __name__ == "__main__":
    logger.basicConfig(level=logging.DEBUG, filename="st.log", format="%(asctime)s - %(name)s - %(name)s - %(levelname)s - %(message)s", datetime="%H:%M:%S")
    logger.info("Started divider server")
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)