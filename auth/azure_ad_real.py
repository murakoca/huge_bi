import msal
from flask import session, redirect, url_for, request
from functools import wraps

# Azure portalda oluşturduğunuz uygulama kaydı bilgileri
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
AUTHORITY = "https://login.microsoftonline.com/your_tenant_id"
REDIRECT_URI = "http://localhost:8050/auth/callback"
SCOPE = ["User.Read"]

def login_required_ad(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'azure_user' not in session:
            return redirect(url_for('azure_login'))
        return f(*args, **kwargs)
    return decorated

def azure_login():
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    auth_url = msal_app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return redirect(auth_url)

def azure_callback():
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    code = request.args.get('code')
    result = msal_app.acquire_token_by_authorization_code(code, scopes=SCOPE, redirect_uri=REDIRECT_URI)
    if "id_token_claims" in result:
        session['azure_user'] = result['id_token_claims']
        session['tenant_id'] = result['id_token_claims'].get('tid')  # tenant ID
    return redirect('/dashboard/')