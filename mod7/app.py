import logging.config
from logging_config import dict_config
from flask import Flask
from calculator import addition_numbers, subtracting_numbers

app = Flask(__name__)
logging.config.dictConfig(dict_config)
logger = logging.getLogger('web_data')


@app.route('/sum/<path:numbers>', methods=['GET'])
def web_sum(numbers):
    if data_processing(numbers):
        numbers = data_pars(numbers)
        return str(addition_numbers(numbers))
    return "Incorrect data has been entered, try again. Example: '.../diff/23/5'"


@app.route('/diff/<path:numbers>', methods=['GET'])
def web_diff(numbers):
    if data_processing(numbers):
        numbers = data_pars(numbers)
        return str(subtracting_numbers(numbers))
    return "Incorrect data has been entered, try again. Example: '.../diff/23/5'"


def data_processing(numbers: str) -> bool:
    try:
        data_pars(numbers)
    except ValueError as ex:
        logger.warning("Error in the data", exc_info=ex)
        return False

    if 0 <= len(numbers) <= 1:
        logger.exception("One number is not enough to perform the action")
        return False

    return True


def data_pars(numbers: str) -> list[float]:
    return list(map(float, numbers.split('/')))


if __name__ == '__main__':
    app.run(debug=True)