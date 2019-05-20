# Servers and Handlers
Web servers using http.server are made of two parts:
    1. the HTTPServer class, and 
    2. a request handler class. 
    
> The first part, the `HTTPServer class`, is built into the module and 
is the same for every web service.

> It knows how to listen on a port and accept HTTP requests from clients. 
Whenever it receives a request, it hands that request off to 
**the second part** — a request handler — which is different for every web service.
Here it is `HelloServer class` the handler class.
