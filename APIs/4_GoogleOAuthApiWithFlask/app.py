from flask import Flask, render_template
import json
import secrets
import google_auth
import google_drive

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.register_blueprint(google_auth.app)
app.register_blueprint(google_drive.app)


@app.route('/')
def index():
    if google_auth.is_logged_in():
        drive_fields = "files(id,name,mimeType,createdTime,modifiedTime,shared,webContentLink)"
        items = google_drive.build_drive_api_v3().list(
            pageSize=20, orderBy="folder", q='trashed=false',
            fields=drive_fields
        ).execute()
        return render_template('list.html', files=items['files'], user_info=google_auth.get_user_info())
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8040)
