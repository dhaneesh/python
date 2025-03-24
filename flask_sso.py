from flask import Flask, redirect, request, session, url_for, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Keycloak Configuration
KEYCLOAK_URL = "http://localhost:8080"
REALM = "myrealm"
CLIENT_ID = "flask-client"
CLIENT_SECRET = "7eXYUIPbK8cet1AH9qdYWni0Zs29fuzX"  # Replace with actual secret if needed
REDIRECT_URI = "http://127.0.0.1:5000/callback"
FASTAPI_URL = "http://127.0.0.1:8000"

@app.route("/")
def home():
    if "access_token" in session:
        return redirect(url_for("dashboard"))
    return '<a href="/login">Login with Keycloak</a>'

@app.route("/login")
def login():
    """Redirects user to Keycloak login."""
    auth_url = (
        f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/auth"
        f"?client_id={CLIENT_ID}&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """Handles Keycloak callback, exchanges code for token."""
    code = request.args.get("code")
    if not code:
        return "Error: No authorization code provided", 400

    token_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,  # Remove if not using client secret
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        session["access_token"] = token_data["access_token"]
        return redirect(url_for("dashboard"))
    return "Error exchanging code for token", 400

@app.route("/dashboard")
def dashboard():
    """Displays user info after login."""
    if "access_token" not in session:
        return redirect(url_for("login"))

    access_token = session["access_token"]
    print("where is access token")
    print(access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{FASTAPI_URL}/protected", headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    return "Access Denied", 403

@app.route("/logout")
def logout():
    """Logs out user by redirecting to Keycloak logout."""
    session.clear()
    logout_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/logout?redirect_uri=http://127.0.0.1:5000"
    return redirect(logout_url)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
