from flask import Flask
import subprocess

app = Flask(__name__)


@app.route("/uptime")
def show_work_time():
    uptime = str(subprocess.check_output(['uptime']))
    uptime = uptime.split()[3][:-1]
    return f'Current uptime is {uptime}'


if __name__ == "__main__":
    app.run()