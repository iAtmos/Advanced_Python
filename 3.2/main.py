from flask import Flask
import sys

app = Flask(__name__)


@app.route('/decoder/<string:s>')
def decrypt(s):
    list_symbols = []

    for ch in s:
        list_symbols.append(ch)

        if len(list_symbols) > 2 and (list_symbols[-1], list_symbols[-2]) == ('.', '.'):
            list_symbols.pop()
            list_symbols.pop()
            if list_symbols:
                list_symbols.pop()

    result = "".join(ch for ch in list_symbols if ch != '.')

    if result:
        return result
    else:
        return '<пустая строка>'


if __name__ == "__main__":
    app.run(debug=True)