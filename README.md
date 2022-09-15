# Temperature Conversion API

## Usage

The API is called using a query string.  The key `c` is used to specify a Celsius temperature to be converted to Fahrenheit, and the key `f` is used to convert from Fahrenheit to Celsius.  The following examples assume that the API endpoint is at `http://localhost/temperature`.

### Convert Celsius to Fahrenheit
#### Request

`GET localhost/temperature?c=100`

    > curl localhost/temperature?c=100

#### Response
    212.0
    
### Convert Fahrenheit to Celsius
#### Request

`GET localhost/temperature?f=32`

    > curl localhost/temperature?f=32

#### Response
    0.0
    


## Deployment

### Standalone Server
The WSGI script doubles as a standalone server.  Simply run the script to spawn a server on port 8080.  The port number can be changed by modifying the `PORT` variable in the script.

`python temperature.wsgi`

### Apache + mod_wsgi
If you have an apache server with mod_wsgi installed, add an endpoint to your `httpd.conf` file.  For example:

`WSGIScriptAlias /temperature /usr/local/www/wsgi-scripts/temperature.wsgi`

## Design Discussion

In the process of implementing this temperature conversion API, I made several design decisions:

The first decision is to use Python.  I use Python on a daily basis, so it best demonstrates my technical skill, and it is well suited to projects like this one.  Implementing a project in Python ensures that the code will be easy to read, understand, and maintain, and that there will be a large number of potential programmers available if more developers are needed to work on it.

After this, I decided to implement the API as a simple WSGI script.  Python has many web frameworks available, but none is necessary for a simple temperature conversion.  My implementation depends on nothing outside of Python’s standard library.  This greatly simplifies deployment, eliminates overhead that these frameworks may incur, and allows developers without knowledge of these frameworks to work on the project.  We have flexibility to deploy using any combination of WSGI server and web server, and the API can be scaled to any number of users by simply increasing the number of servers.

Next, I decided to format the API interface so that URLs would be short and could be processed quickly.  An API request is called by using a query string that contains a key of `c` or `f` (for Fahrenheit or Celsius, respectively) and a value for the corresponding temperature in the usual formatting for a floating point number.  The response is similarly formatted as a floating point number.  If both temperature scales are specified, the first Celsius temperature specified is used.  If more than one temperature value is specified for a scale, all but the first are ignored.  An error response is returned if no temperature is specified, or if the temperature specified cannot be interpreted as a float.  The Python float type is used when attempting to convert the temperature value and presents no security problems.

I chose not to follow the REST format for API requests.  REST is a useful conceptual framework for organizing interaction with objects via an API, but for a simple temperature conversion it adds little benefit.  Similarly, I decided against formatting the response as JSON or some other structured format.  This eliminates the overhead involved in packing the value into JSON and unpacking it on the user end.  All of these decisions make processing an API request as simple and fast as possible.
