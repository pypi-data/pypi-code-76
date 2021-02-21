from BlackBlazefw import webApp
from FileRenderer import FileRenderer

app = webApp("__init__", "GUNICORN")
renderfile = FileRenderer()

@app.catchURL('/hello/100')
def hello(response):
    response.status_code = 200
    response.text = "HELLO"
@app.catchURL('/hello/200')
def hello(response):
    response.status_code = 200
    response.text = "HELLO"
@app.catchURL('/hello/300')
def hello(response):
    response.status_code = 300
    response.text = renderfile.render("index.html")

app.setError(404, "404.html")