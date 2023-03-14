from flask import Flask

app = Flask(__name__)
units_name = ["бит", "байт", "КБайт", "МБайт", "ГБайт", "ТБайт", "ПБайт"]
result = ""


@app.route('/rss/<path:file_path>')
def get_summary_rss(file_path):
    sum_rss = 0

    with open(file_path, 'r', encoding='utf-8') as book:
        book = book.readlines()[1:]

        for i_line in book:
            if not i_line.split():
                continue
            sum_rss += float(i_line.split()[5])

    return translation_bit(sum_rss)


def translation_bit(sum_rss, units=8, iteration=0):
    global result
    if sum_rss // units > 1:
        translation_bit((sum_rss / units), 1024, (iteration + 1))
        return result
    else:
        result = "Затраты памяти составляют: {:.2f} {}".format(sum_rss, units_name[iteration])


if __name__ == "__main__":
    app.run(debug=True)