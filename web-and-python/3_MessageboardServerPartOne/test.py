# Test script for the Messageboard Part One server.
#
# The server should be listening on port 8000 and answer a POST request
# with an echo of the "message" field.

import requests, random, socket

def test_connect():
    '''Try connecting to the server.'''
    print("Testing connecting to the server.")

    try:
        with socket.socket() as s:
            s.connect(("localhost", 8000))
        print("Connection attempt succeeded.")
        return None
    except socket.error:
        return "Server didn't answer on localhost port 8000.  Is it running?"

def test_POST():
    '''The server should accept a POST and return the "message" field.'''
    print("Testing POST request.")
    msg = random.choice(["Hey there!", "Morning!", "Greetings!"])
    uri = "http://localhost:8000/"

    try:
        req = requests.post(uri, data = {'message': msg})
    except requests.RequestException as e:
        return ("Couldn't communicate with the server. ({})\n"
            "If it's running, take a look at its output.").format(e)

    if req.status_code == 501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a POST request.\n"
                "(Is the correct server code running?)")
    elif req.status_code != 200:
        return ("The server returned status code {} instead of a 200 OK."
                ).format(req.status_code)
    elif req.text != msg:
        return ("The server sent a 200 OK response, but the content differed.\n"
                "I expected '{}' but it sent '{}'.").format(msg, req.text)
    else:
        print("POST request succeeded.")
        return None


if __name__ == "__main__":
    tests = [test_connect, test_POST]
    for test in tests:
        error = test()
        if error is not None:
            print(error)
            break
    print("All tests succeeded!")
