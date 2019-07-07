# Google OAuth API with Flask
we'll create a Python app using Flask and the Google API which will:

1. Support Google Authentication with Python and Flask
2. Restrict access via an OAuth scope, so that the app can only view and manage Google Drive files and folders which were created by the app
3. Read and write files on the user’s Google Drive with Python.

By the time you get to the end of this blog post, you’ll have built 
a basic Google Drive file browser.


## Prerequisites
Make sure you have a Google account before you start.

## Running Steps
1. Start Flask via `app.py`, and in your browser, navigate to `http://localhost:8040`.
2. With the Flask app up and running, navigate to `http://localhost:8040/google/login`, 
and you should be redirected to the Sign in with Google screen.
3. To log out, navigate to `http://localhost:8040/google/logout`.