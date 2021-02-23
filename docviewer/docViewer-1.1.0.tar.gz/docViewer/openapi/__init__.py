import os
from pathlib import Path
from flask import Flask, render_template, send_file
app = Flask(__name__)


@app.route('/')
def swagger_ui():
    return render_template('swagger-ui.html')


@app.route('/editor')
def swagger_editor():
    return render_template('swagger-editor.html')


@app.route('/redoc')
def redoc():
    return render_template('redoc.html')


@app.route('/openapi.yaml')
def doc_file():
    doc_path = Path(os.environ['API_DOC'])
    doc_path = Path.cwd().joinpath(doc_path)
    return send_file(doc_path)


if __name__ == '__main__':
    app.run()
