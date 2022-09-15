from urllib.parse import parse_qs

# Entry point for WSGI application
def application(environ, start_response):
    # Default HTTP status
    status = '200 OK'
    
    # Parse the query string
    query = parse_qs(environ['QUERY_STRING'])

    # Do Celsius to Fahrenheit conversion
    if 'c' in query:
        try:
            temp = float(query['c'][0])
            temp = temp*(9/5) + 32
            response_body = str(temp)
        except ValueError as error:
            # Unable to convert temperature
            status = '400 Bad Request'
            response_body = 'Input could not be interpreted as float.'
    # Do Fahrenheit to Celsius conversion
    elif 'f' in query:
        try:
            temp = float(query['f'][0])
            temp = (temp - 32)*(5/9)
            response_body = str(temp)
        except ValueError as error:
            # Unable to convert temperature
            status = '400 Bad Request'
            response_body = 'Input could not be interpreted as float.'
    else:
        # No temperature arguments were specified.
        status = '400 Bad Request'
        response_body = 'Arguments required.'

    
    # Encode response as UTF-8
    response_body = bytes(response_body, encoding='utf-8')

    # Prepare response
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]
    
if __name__ == '__main__':
    # Use Python's builtin WSGI server
    from wsgiref.simple_server import make_server

    PORT = 8080 # Choose the port for serving application
    httpd = make_server('localhost', PORT, application)

    # Continuously serve requests
    while True:
        httpd.handle_request()