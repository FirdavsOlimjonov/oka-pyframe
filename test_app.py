import pytest
from app import OkaFrameApp


def test_basic_route_adding(app):
    @app.route("/home")
    def home(request, response):    
        response.text = "Welcome Home Firdavs!"


def test_duplicate_route_throws_exception(app):
    @app.route("/home")
    def home(request, response):    
        response.text = "Welcome Home Firdavs!"

    with pytest.raises(AssertionError):
        @app.route("/home")
        def home(request, response):    
            response.text = "Welcome Home Firdavs!"


def test_requests_can_be_sent_by_test_client(app, test_client):
    @app.route("/home")
    def home(request, response):    
        response.text = "Welcome Home Firdavs!"

    response = test_client.get("http://testserver/home")

    assert response.text == "Welcome Home Firdavs!"


def test_parameterized_routing(app, test_client):
    @app.route("/hello/{name}")
    def about(request, response, name):
        response.text = f"Hello {name}"
    
    assert test_client.get("http://testserver/hello/Firdavs").text == "Hello Firdavs"


def test_default_response(app, test_client):
    response = test_client.get("http://testserver/nothing")

    assert response.text == "Not Found!"
    assert response.status_code == 404


def test_class_based_get(app, test_client):
    @app.route("/books")
    class Books: 
        def get(self, req, resp):
            resp.text = "Books page"

    assert test_client.get("http://testserver/books").text == "Books page"


def test_class_based_post(app, test_client):
    @app.route("/books")
    class Books: 
        def post(self, request, response):
            response.text = "Books post method"

    assert test_client.post("http://testserver/books").text == "Books post method"


def test_class_based_method_not_found(app, test_client):
    @app.route("/books")
    class Books: 
        def post(self, request, response):
            response.text = "Books post method"

    response = test_client.get("http://testserver/books")

    assert response.text == "Method not found!"
    assert response.status_code == 405


def test_alternative_adding_route(app, test_client):
    def new_handler(req, resp):
        resp.text = "From new handler"
    
    app.add_route("/new-handler", new_handler)

    assert test_client.get("http://testserver/new-handler").text == "From new handler"


def test_template_handler(app, test_client):
    @app.route("/template")
    def template_handler(req, resp):
        resp.body = app.template(
            "home.html",
            contex={"new_title":"New Title", "new_body":"New Body..."}
        )
    
    response = test_client.get("http://testserver/template")

    assert "New Title" in response.text
    assert "New Body..." in response.text
    assert "text/html" in response.headers["Content-Type"]


def test_custom_exception(app, test_client):
    def on_exception(req, resp, exc):
        resp.text = "Something bad happened"


    app.add_expetion_handler(on_exception)


    @app.route("/exception")
    def exception_throwing_handler(req, resp):
        raise AssertionError("some error")
    
    response = test_client.get("http://testserver/exception")

    assert response.text == "Something bad happened"