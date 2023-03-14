from flask import Flask
import os

app = Flask(__name__)


@app.route('/preview/<int:size>/<path:file_path>')
def preview_symbols(size, file_path):
    file_name = str(file_path).split('/')[-1]
    abs_path = os.path.abspath(file_name)
    file = open(file_path, 'r')

    return "<b>{}</b> {}<br>{}".format(abs_path, size, file.read(size))


if __name__ == "__main__":
    app.run(debug=True)