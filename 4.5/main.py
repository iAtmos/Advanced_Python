from flask import Flask, request
import subprocess, shlex

app = Flask(__name__)


@app.route("/ps/", methods=['GET'])
def get_ps():
    args = request.args.getlist('arg')
    command = shlex.quote(args)

    response = str(subprocess.check_output(['ps', command]).decode())
    return f"<pre>{response}</pre>"


if __name__ == "__main__":
    app.run()