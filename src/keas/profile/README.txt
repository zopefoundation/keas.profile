Keas.profile
------------

Middleware that profiles the request and displays profiling information at the
bottom of each page.

  >>> from email import utils
  >>> from keas.profile import profiler

Lets start with a simple "hello world" app to profile

  >>> def simple_app(environ, start_response):
  ...     start_response('200 OK', [('content-type', 'text/html')])
  ...     return "hello world!"
  ...
  >>> def start_response(status, headers, exc_info=None):
  ...   pass

we can now generate a middleware profiler for the app

  >>> profiled_app = profiler.make_profiler(simple_app, global_conf=None)

and call the app to profile it

  >>> environ = {'HTTP_DATE': utils.formatdate(),
  ...            'PATH_INFO': '/' ,
  ...            'REQUEST_METHOD': 'GET'}

  >>> profiled_app(environ, start_response)
  ['hello world!... function calls in ... CPU seconds...
  ...Ordered by: cumulative time, call count...]

The profiler output is appended to the end of the response body if it returns
HTML.  (Yes, this violates the HTML standard, but seems to work in practice.)
