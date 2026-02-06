from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(_name_)

# 🔐 Secret key for session
app.secret_key = "your_secret_key_here"

# 🔗 OAuth setup
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='166703313280-rm49louvhb8q6v80se3ampicqgi1 ec3h.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={
        'scope': 'email profile'
    }
)

# 🏠 Home page
@app.route('/')
def index():
    if 'user' in session:
        user = session['user']
        return f"""
        <h2>Welcome {user['name']}</h2>
        <p>Email: {user['email']}</p>
        <img src="{user['picture']}" width="100"><br><br>
        <a href="/logout">Logout</a>
        """
    return '''
        <h2>Login Page</h2>
        <a href="/login/google">
            <button>Continue with Google</button>
        </a>
    '''

# 🔐 Google login
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

# 🔁 Google callback
@app.route('/login/google/callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()

    # Save user info in session
    session['user'] = user_info

    return redirect('/')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# ▶ Run app
if _name_ == "_main_":
    app.run(debug=True)