# flaskApp.py

import pandas as pd
from bokeh.client import pull_session
from bokeh.embed import server_session
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/pedropaiva/Downloads/'

disabled = False


# locally creates a page
@app.route('/demo')
def index():
    with pull_session(url="http://localhost:5006/") as session:
        # generate a script to load the customized session
        script = server_session(session_id=session.id, url='http://localhost:5006')
        # use the script in the rendered page
    return render_template("embed.html", script=script, template="Flask")


@app.route('/')
def start():
    return render_template("index.html", dis=disabled)


@app.route('/config', methods=['GET', 'POST'])
def check():
    global disabled
    if request.method == "POST":
        req = request.form
        print(req)
        disabled = not disabled
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                df = pd.read_csv(request.files.get('file'))
                print(df.head())
        return redirect('/demo')
    return render_template("configuration.html")


if __name__ == '__main__':
    # runs app in debug mode
    app.run(port=5000, debug=True)
