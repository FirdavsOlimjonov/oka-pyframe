from app import OkaFrameApp

app = OkaFrameApp()

@app.route("/home")
def home(request, response):
    response.text = "Welcome Home Firdavs!"

@app.route("/about")
def about(request, response):
    response.text = "About me..."

@app.route("/hello/{name}")
def about(request, response, name):
    response.text = f"Hello {name}"


@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "Books get method..."

    def post(self, request, response):
        response.text = "Books post method..."


def new_handler(req, resp):
    resp.text = "From new handler"

app.add_route("/new-handler", new_handler)


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template(
        "home.html",
        contex={"new_title":"New Title", "new_body":"New Body..."}
    )


def on_exception(req, resp, exc):
    resp.text = "Something bad happened"


app.add_expetion_handler(on_exception)


@app.route("/exception")
def exception_throwing_handler(req, resp):
    raise AssertionError("some error")