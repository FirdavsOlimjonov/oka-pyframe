
from typing import Any
from webob import Request, Response
from parse import parse
import inspect
import requests
import wsgiadapter


class OkaFrameApp:

    def __init__(self):
        self.routes = dict()

    def __call__(self, environ, start_response):
       request = Request(environ)
       response = self.handle_request(request)

       return response(environ, start_response)
    

    # def handle_request(self, request):
    #     response = Response()
    #     handler_data, kwargs = self.find_handler(request)

    #     if handler_data is not None:
    #         handler = handler_data["handler"]
    #         allowed_methods = handler_data["allowed_methods"]

    #         if inspect.isclass(handler):
    #             handler = getattr(handler(), request.method.lower(), None)
    #             ic(handler)

    #             if handler is None:
    #                 return self.method_not_allowed(response)
    #         else:
    #             if request.method.lower() not in allowed_methods:
    #                 return self.method_not_allowed(response)

    #         try:
    #             handler(request, response, **kwargs)
    #         except Exception as e:
    #             if self.exception_handler is not None:
    #                 self.exception_handler(request, response, e)
    #             else:
    #                 raise e
    #     else:
    #         self.default_response(response)
    #     return response

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
                
            handler(request, response, **kwargs)
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
    
    
    def route(self, path):
        assert path not in self.routes, "Duplicate route, please change the URL."

        # if path in self.routes:
        #     raise AssertionError("Duplicate route, please change the URL.")

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
        return wrapper
    

    def test_session(self):
        session = requests.Session()
        session.mount("http://testserver", wsgiadapter.WSGIAdapter(self))
        return session


