from flask import Flask, Response, send_file
import time
import os
import tempfile
import pollingserver.write_csvs


cache_dir = os.path.join(tempfile.gettempdir(), "pollingserver")
if not os.path.isdir(cache_dir):
    os.mkdir(cache_dir)
    os.chmod(cache_dir, 0o755)


application = Flask(__name__)


updatetime = 3600


def _update_files():
    filepath = os.path.join(cache_dir, "parties.csv")

    now = time.time()
    update_needed = True
    if os.path.isfile(os.path.join(cache_dir, filepath)):
        mod_time = os.path.getmtime(filepath)
        if now - mod_time < updatetime:
            update_needed = False

    if update_needed:
        pollingserver.write_csvs.write_csvs(cache_dir)


@application.route('/file/<selection>')
def send_attachment(selection):
    _update_files()

    filepath = os.path.join(cache_dir, selection)
    if os.path.isfile(filepath):
        return send_file(filepath)
    return "No data found"


@application.route('/data/<selection>')
def send_data(selection):

    if selection not in pollingserver.write_csvs.available_data():
        return "No data found"

    _update_files()

    filename = pollingserver.write_csvs.filename_from_string(selection)
    filepath = os.path.join(cache_dir, filename)

    with open(filepath, "r") as f:
        text = f.read()

    return Response(text, mimetype="text/plain")


@application.route('/hello_world')
def hello_world():
    return 'Hello World!'


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
