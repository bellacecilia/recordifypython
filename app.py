from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = ""
CLIENT_SECRET = ""
TOKEN_CODE = "token_info"
SECRET_KEY = ""


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    name = 'username'
    return render_template('index.html', title='Welcome', username=name)

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth (
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-top-read user-library-read"
    )

    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirectPage')
def redirectPage():
    code = request.args.get('code')
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-top-read user-library-read"
    )
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_CODE] = token_info
    return redirect(url_for("record", _external=True))

def get_token():
    token_info = session.get(TOKEN_CODE, None)
    return token_info

@app.route('/record')
def record():
    user_token = get_token()
    sp = spotipy.Spotify(
        auth  = user_token['access_token']
    )
    current_user_name = sp.current_user()['display_name']
    short_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="short_term",
    )
    medium_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="medium_term",
    )
    long_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="long_term",
    )
    return render_template('record.html', user_display_name=current_user_name, short_term=short_term, medium_term=medium_term, long_term=long_term)