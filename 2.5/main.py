import sys

from flask import Flask

app = Flask(__name__)


@app.route('/max_number/<path:line>')
def max_number(line):
    numbers = str(line).split('/')
    max_value = -sys.maxsize

    for i_number in numbers:
        if i_number.isdigit():
            max_value = max(float(i_number), max_value)
    else:
        if max_value == -sys.maxsize:
            return "Вы не ввели ни одного числа!"
    return f"Максимальное число: <i>{max_value}</i>"


if __name__ == "__main__":
    app.run(debug=True)