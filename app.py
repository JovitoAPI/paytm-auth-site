from flask import Flask, redirect, request, render_template_string
import os

app = Flask(__name__)

# Load keys from environment variables (set them later in Render dashboard)
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "your_client_id_here")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "your_client_secret_here")
REDIRECT_URI = "https://paytm-auth-site.onrender.com/callback"

@app.route("/")
def home():
    # Button for user to authorize
    auth_url = (
        f"https://developer.paytmmoney.com/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )
    return render_template_string("""
        <h2>🚀 Paytm Money Authorization</h2>
        <a href="{{ auth_url }}">
            <button>Authorize with Paytm Money</button>
        </a>
    """, auth_url=auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "⚠️ No code received"
    return f"<h2>✅ Authorization Successful</h2><p>Your code: <b>{code}</b></p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
