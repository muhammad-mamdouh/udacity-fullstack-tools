from flask import Flask, render_template
import json
import secrets
import google_auth

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.register_blueprint(google_auth.app)


@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + \
               user_info['given_name'] + '<div><pre>' + \
               json.dumps(user_info, indent=4) + "</pre>"
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8040)
