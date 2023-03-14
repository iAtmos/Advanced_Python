from flask import Flask
from datetime import datetime

app = Flask(__name__)
days = ('Хорошего понедельника!', 'Хорошего вторника!', 'Хорошей среды!', 'Хорошего четверга!', 'Хорошей пятницы!', 'Хорошей субботы!', 'Хорошего воскресенья!')


@app.route('/hello-world/<string:name>')
def greeting(name):
    weekday = datetime.today().weekday()
    return "Привет, {}. {}".format(name, days[weekday])


if __name__ == "__main__":
    app.run(debug=True)