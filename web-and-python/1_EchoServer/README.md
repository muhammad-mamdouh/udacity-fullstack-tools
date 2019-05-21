# Echo server

This new server will also listen on port 8000,
but it will respond to GET requests by repeating back ("echoing") the text
of the request path.

To test the code, you'll need two terminals open:  
In one of them, run the server ( with `python3 EchoServer.py` ).  
You can then access it from your browser, for instance at http://localhost:8000/GoodMorningHTTP.  
In the other terminal, run the test script provided (`python3 test.py`).  The test
script will send a request to the server and tell you whether it worked.

