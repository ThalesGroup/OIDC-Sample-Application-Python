import json
import logging

from flask import Flask, g, render_template, session, make_response
from flask_oidc import OpenIDConnect, request
import webbrowser
import requests
from urllib.parse import urljoin
import constant

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.update({
     'SECRET_KEY': 'd3812c94-01b4-4c55-a746-44688a087664',
     'Debug':True,
     'OIDC_CLIENT_SECRETS': 'client_secrets.json',
     'OIDC_ID_TOKEN_COOKIE_SECURE': False,
     'OIDC_REQUIRE_VERIFIED_EMAIL': False,
     'OIDC_USER_INFO_ENABLED': True,
     'OIDC_OPENID_REALM': '8K74HMZZ9R-STA',
     'OIDC_SCOPES': ['openid', 'email', 'profile'],
     'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})

oidc = OpenIDConnect(app)

@app.route('/', methods=['GET', 'POST'])
def startup_login_oidc():
    if oidc.user_loggedin:
                return render_template(constant.templateName)
    else:
        return oidc.redirect_to_auth_server(constant.localServerName)

@app.route('/login', methods=['GET', 'POST'])
@oidc.require_login
def login_oidc():

    info = oidc.user_getinfo(constant.userInfo)

    user_id = info.get('sub')

    if user_id in oidc.credentials_store:
        try:
            from oauth2client.client import OAuth2Credentials
            access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
            id_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).id_token
            refresh_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).refresh_token
            print ('access_token=<%s>' % access_token)
            print ('id_token=<%s>' % id_token)
            print ('refresh_token=<%s>' % refresh_token)
        except:
             print ("Something went wrong. Please contact Author of the App")

    return render_template(constant.templateName)

@app.route('/Logout', methods=['GET', 'POST'])
def logout():
    info = oidc.user_getinfo(constant.userInfo)

    user_id = info.get('sub')

    if user_id in oidc.credentials_store:
        try:
            from oauth2client.client import OAuth2Credentials
            refresh_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).refresh_token
        except:
             print ("Something went wrong. Please contact Author of the App")
   
    oidc.logout()
    logout_idp(refresh_token)  
    return oidc.redirect_to_auth_server(constant.localServerName)

def logout_idp(refresh_token,  **kwargs):
     clientConfig = oidc.client_secrets
     path = {"realm-name": clientConfig["realm_name"]}
     data = {"client_id": clientConfig["client_id"], "refresh_token": refresh_token, "client_secret": clientConfig["client_secret"]}
     URL_LOGOUT = "realms/{realm-name}/protocol/openid-connect/logout"
     
     try:
          info = requests.post(urljoin(clientConfig["base_url"], URL_LOGOUT.format(**path)),
                   params=kwargs,
                   data=data,
                   headers={},
                   timeout=60,
                   verify=True)
     except:
         print ("Something went wrong in Logout. Please contact Author of the App")

if __name__ == '__main__':
    app.run()
