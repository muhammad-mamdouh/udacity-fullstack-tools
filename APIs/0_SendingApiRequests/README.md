# APISERVER Web Server
This is a flask based web server for testing the types of responses
using CURL tool.

>All of the next commands are typed in a UNIX based shell

## Requirements
Open your terminal and type this command
```
pip3 install flask
```

## Run the server
```
python3 ApiServer.py
```

### Keep the server up, and open another terminal to test the API endpoints
1. Sending HTTP GET Request
```
curl localhost:5000/readHello -i
```

2. Sending HTTP POST Request
```
curl -X POST localhost:5000/createHello -i
```

3. Sending HTTP PUT Request
```
curl -X PUT localhost:5000/updateHello -i
```

4. Sending HTTP DELETE Request
```
curl -X DELETE localhost:5000/deleteHello -i
```
