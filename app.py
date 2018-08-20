# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, url_for

import requests
import json

# for secret key
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key

client_id = config.client_id
client_secret = config.client_secret

OAUTH2_URL = "https://apiv2.twitcasting.tv/oauth2"
CATEGORY_URL = "https://apiv2.twitcasting.tv/categories"


def login_url(ci):
    return OAUTH2_URL + "/authorize?client_id={YOUR_CLIENT_ID}&response_type=code".format(**{"YOUR_CLIENT_ID": ci})


@app.route('/callback')
def callback():
    code = request.args.get("code")
    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://localhost:5000/callback"
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = requests.post(OAUTH2_URL+"/access_token", data=payload, headers=headers)
    if req.status_code != 200:
        print(req.text)
        raise req.text
    data = json.loads(req.text)
    session["access_token"] = data["access_token"]
    return redirect(url_for('index'))


@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token:
        return access_token
    else:
        return render_template('index.html', sign_in=login_url(client_id), text="login")


if __name__ == '__main__':
    app.debug = True
    app.run()
