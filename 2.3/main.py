from flask import Flask
import sys

app = Flask(__name__)


@app.route('/decoder')
def decrypt():
    filter_symbol = '.'
    decrypt_str = ''
    index_start_buffer = -1
    buffer = 0

    lines = sys.stdin.read()

    for i_index, i_symbol in enumerate(lines):
        if i_symbol not in filter_symbol:
            decrypt_str = "{}{}".format(decrypt_str, i_symbol)
        else:
            if buffer == 0:
                index_start_buffer = i_index
                buffer += 1
                continue
            elif buffer == 1:
                if index_start_buffer + 1 == i_index:
                    decrypt_str = decrypt_str[:-1]
                    buffer = 0
                else:
                    index_start_buffer = i_index
    else:
        if len(decrypt_str) == 0:
            return "<пустая строка>"

    return decrypt_str


if __name__ == "__main__":
    app.run(debug=True)