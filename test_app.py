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


# def test_class_based_post(app, test_client):
#     @app.route("/books")
#     class Books: 
#         def post(self, request, response):
#             response.text = "Books post method"

#     assert test_client.post("http://testserver/books").text == "Books post method"
