from flask import Flask, Response
import time
import os
import tempfile
import pollingserver.write_csvs


cache_dir = os.path.join(tempfile.gettempdir(), "pollingserver")
if not os.path.isdir(cache_dir):
    os.mkdir(cache_dir)
    os.chmod(cache_dir, 0o755)


app = Flask(__name__)


updatetime = 3600


@app.route('/data/<selection>')
def send_data(selection):

    if selection not in pollingserver.write_csvs.available_data():
        return "No data found"

    filename = pollingserver.write_csvs.filename_from_string(selection)
    filepath = os.path.join(cache_dir, filename)

    now = time.time()
    update_needed = True
    if os.path.isfile(os.path.join(cache_dir, filepath)):
        mod_time = os.path.getmtime(filepath)
        if now - mod_time < updatetime:
            update_needed = False

    if update_needed:
        pollingserver.write_csvs.write_csvs(cache_dir)

    with open(filepath, "r") as f:
        text = f.read()

    return Response(text, mimetype="text/plain")


@app.route('/hello_world')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
