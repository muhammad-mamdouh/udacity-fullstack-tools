import os
import functools
from flask import Blueprint, redirect, request, make_response, flash
from flask import session as login_session
from flask_login import logout_user
from authlib.client import OAuth2Session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
AUTHORIZATION_SCOPE = 'openid email profile https://www.googleapis.com/auth/drive.file'
AUTH_REDIRECT_URI = 'http://localhost:5000/google/auth'
BASE_URI = 'http://localhost:5000'
CLIENT_ID = '585155461752-plmkfmgjco98avdd4rqebvlopdggn0rr.apps.googleusercontent.com'
CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET", default=False)
AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

app = Blueprint('google_auth', __name__)


def is_logged_in():
    if ACCESS_TOKEN_URI in login_session:
        user_info = get_user_info()
        login_session['gplus_id'] = user_info['id']
        login_session['username'] = user_info['given_name']
        login_session['picture'] = user_info['picture']
        login_session['email'] = user_info['email']
        return True
    else:
        return False


def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')
    oauth2_tokens = login_session[AUTH_TOKEN_KEY]
    return Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI)


def get_user_info():
    credentials = build_credentials()
    oauth2_client = build('oauth2', 'v2', credentials=credentials)
    return oauth2_client.userinfo().get().execute()


def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)


@app.route('/google/login')
@no_cache
def login():
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)
    uri, state = session.authorization_url(AUTHORIZATION_URL)
    login_session[AUTH_STATE_KEY] = state
    login_session.permanent = True
    flash("You're now logged in successfully!")
    return redirect(uri, code=302)


@app.route('/google/auth')
@no_cache
def google_auth_redirect():
    req_state = request.args.get('state', default=None, type=None)

    if req_state != login_session[AUTH_STATE_KEY]:
        response = make_response('Invalid state parameter', 401)
        return response

    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state=login_session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
        ACCESS_TOKEN_URI,
        authorization_response=request.url)
    login_session[AUTH_TOKEN_KEY] = oauth2_tokens
    return redirect(BASE_URI, code=302)


@app.route('/google/logout')
@no_cache
def logout():
    login_session.pop(AUTH_TOKEN_KEY, None)
    login_session.pop(AUTH_STATE_KEY, None)
    login_session.pop('gplus_id', None)
    login_session.pop('email', None)
    login_session.pop('username', None)
    login_session.pop('picture', None)
    flash("We're waiting for you to come back soon!")
    logout_user()
    return redirect(BASE_URI, code=302)
