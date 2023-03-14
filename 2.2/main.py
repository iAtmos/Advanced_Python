from flask import Flask
import sys

app = Flask(__name__)


@app.route('/pipe')
def get_mean_size():
    sum_rss = 0
    lines = sys.stdin.readlines()[1:]

    for i_line in lines:
        sum_rss += int(i_line.split()[4])
    else:
        if len(lines) == 0 or sum_rss:
            return "Отсутвутют файлы"

    return "Средний размер файла: {}".format((sum_rss / len(lines)))


if __name__ == "__main__":
    app.run(debug=True)