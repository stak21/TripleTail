#!/usr/bin/python3
"""Start Flask web app for our TripleTail
website"""

from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS, cross_origin
from user import User

import requests
import os

# Flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
host = '0.0.0.0'
host = '127.0.0.1'
# Cross-Origin Resource sharing
cors = CORS(app, resouces={r"/*": {"origins": "*"}})

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
request_url = 'https://api.github.com'
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

def page_not_found(e):
    """404 error page for nonexistent routes"""
    return jsonify({'error': "Not found"}), 404


@app.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Landing page
    """
    if request.method == 'POST':
        return redirect("https://github.com/login/oauth/authorize?client_id={}".format(client_id));
    return render_template('index.html')


@app.route('/testing')
def test():
    userinfo = {'tier': 'tier1', 'username': 'hello', 'name': 'Random Name', 'public_repos': 10,        'followers': 10, 'hireable': 'Yes'}
    return render_template('ranking.html', userinfo=userinfo)


@app.route('/tier', methods=['GET', 'POST'])
def handle_callback():
    """
    This function helps exchange temporary 'code' value with a permanent
    access_token.
    """

    if 'code' in request.args:
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': request.args['code']
        }
        headers = {'Accept': 'application/json'}
        req = requests.post(token_url, params=payload, headers=headers)
        resp = req.json()
        if 'access_token' in resp:
            user_info = User(resp['access_token'])
            print(user_info.__dict__)
            return render_template('ranking.html', userinfo=user_info.__dict__)
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_error_handler(404, page_not_found)
    app.run(host=host)
