
from webob import Request, Response
from parse import parse
import inspect
import requests
import wsgiadapter
from jinja2 import Environment, FileSystemLoader
import os
from whitenoise import WhiteNoise


class OkaFrameApp:

    def __init__(self, templates_dir="templates", static_dir="static"):
        self.routes = dict()

        self.template_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

        self.exception_handler = None

        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)


    def __call__(self, environ, start_response):
      return self.whitenoise(environ, start_response)
    

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)


    def handle_request(self, request):
        response = Response()
        
        handler, kwargs = self.find_handler(request)

        if handler is not None:
            if inspect.isclass(handler):
                handler_function = getattr(handler(), request.method.lower(), None)

                if handler_function is None: 
                    response.status_code = 405
                    response.text = "Method not found!"
                    return response
                else:
                     handler_function(request, response, **kwargs)
            else: 
                try:  
                    handler(request, response, **kwargs)
                except Exception as e:
                    if self.exception_handler is not None:
                        self.exception_handler(request, response, e)
                    else:
                        raise e
        else: 
            self.defult_response(response)

        return response


    def find_handler(self, request):
        for path, handler in self.routes.items():
            parsed_result = parse(path, request.path)
            
            if parsed_result is not None:
                return handler, parsed_result.named
        
        return None, None


    def defult_response(self, response):
        response.text = "Not Found!"
        response.status_code = 404
    

    def add_route(self, path, handler):
        assert path not in self.routes, "Duplicate route, please change the URL."
        self.routes[path] = handler
    

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        
        return wrapper
    

    def test_session(self):
        session = requests.Session()
        session.mount("http://testserver", wsgiadapter.WSGIAdapter(self))
        return session


    def template(self, template_name, contex=None):
        if contex is None:
            contex = {}
        
        return self.template_env.get_template(template_name).render(**contex).encode()


    def add_expetion_handler(self, handler):
        self.exception_handler = handler