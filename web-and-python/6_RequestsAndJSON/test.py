#
# Test script for UINames.py

import sys, re, traceback

try:
    import requests
except ImportError:
    print("You need to install the requests module.")
    sys.exit(1)

try:
    import UINames
except ImportError:
    print("Couldn't find your UINames.py code.")
    sys.exit(1)

try:
    str = UINames.SampleRecord()
except IndexError:
    traceback.print_exc()
    print()
    print("Make sure you're providing the three JSON fields in SampleRecord!")
    sys.exit(1)

pattern = re.compile('My name is (\S+) (\S+) and the PIN on my card is (\S+).')
matched = pattern.match(str)

if not matched:
    print("Output didn't look quite right:")
    print(str)
    sys.exit(1)

print("Tests pass!  Here are the fields I found in cardyour code's output:")
print("Name:",    matched.group(1))
print("Surname:", matched.group(2))
print("PIN:",     matched.group(3))