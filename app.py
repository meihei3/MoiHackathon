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

BASE_URL = "https://apiv2.twitcasting.tv"
OAUTH2_URL = BASE_URL + "/oauth2"
CATEGORY_URL = BASE_URL + "/categories"
COMMENT_URL = BASE_URL + "/movies/{movie_id}/comments"
USER_URL = BASE_URL + "/users/{user_id}"


def login_url(ci):
    return OAUTH2_URL + "/authorize?client_id={YOUR_CLIENT_ID}&response_type=code".format(**{"YOUR_CLIENT_ID": ci})


def macro_header(access_token):
    return {"X-Api-Version": "2.0", "Authorization": "Bearer %s" % access_token}


def url2user(url, at):
    """
    URLからuser objectを返す

    :param url: living url
    :param at: access_token
    :return:
    """
    user_id = url.split("/")[-1]
    req = requests.get(USER_URL.format(**{"user_id": user_id}), headers=macro_header(at))
    return json.loads(req.text)


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


@app.route('/comment')
def comment():
    movie_id = request.args.get("movie_id")
    access_token = session.get('access_token')
    headers = macro_header(access_token)
    payload = {"limit": 15}
    req = requests.get(COMMENT_URL.format(**{"movie_id": movie_id}), data=payload, headers=headers)
    print("comment", req.text)
    data = json.loads(req.text)
    return render_template('comment.html', data=data)


@app.route('/user')
def user():
    user_id = request.args.get('user_id')
    access_token = session.get('access_token')
    headers = macro_header(access_token)
    req = requests.get(USER_URL.format(**{"user_id": user_id}), headers=headers)
    print("user:", req.text)
    return req.text


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
