#
# Client for the UINames.com service.
#
# Output:
# My name is Tyler Hudson and the PIN on my card is 4840.

import requests

def SampleRecord():
    req = requests.get("http://uinames.com/api?ext&region=United%20States",
                     timeout=2.0)

    # Decode JSON from the response.
    data = req.json()

    return "My name is {} {} and the PIN on my card is {}.".format(
        data["name"],
        data["surname"],
        data["credit_card"]["pin"]
    )

if __name__ == '__main__':
    print(SampleRecord())