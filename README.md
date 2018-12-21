# OIDC-Sample-Application-Python
This sample code will help customer's integrating their third party solution with Gemalto's Access management(STA) solution using OIDC protocol.

# Prerequisites
1. Python 3.7.0
2. A text editor or code editor of your choice.
3. You already created a Application in your Identity Provider(IDP) and have ClientId, ClientSecret, Authority URL

# Configuring the Application
1. open ../OIDCSampleApplicationPython/client_secrets.json in the text Editor
2. Configure ClientId, ClientSecret, issuer, {IDP hostname}, {RealmName} and other info
3. Ex: 
4. 			 {
        "issuer": "https://{IDP hostname}/auth/realms/{RealmName}",
        "auth_uri": "https://{IDP hostname}/auth/realms/{RealmName}/protocol/openid-connect/auth",
        "client_id": "{ClientId}",
        "client_secret": "{ClientSecret}",
        "userinfo_uri": "https://{IDP hostname}/auth/realms/{RealmName}/protocol/openid-connect/userinfo",
        "token_uri": "https://{IDP hostname}/auth/realms/{RealmName}/protocol/openid-connect/token",
        "token_introspection_uri": "https://{IDP hostname}/auth/realms/{RealmName}/protocol/openid-connect/token/introspect",
        "realm_name": "{RealmName}",
        "base_url": "https://{IDP hostname}/auth/"
    }
4. Ex for "issuer": "http://100.123.12.11/auth/realms/MyOIDCRealm"
5. open ../OIDCSampleApplicationPython/app.py in the text Editor
6. Configure ClientSecret and Realm name in app setting  
7. EX:  app.config.update({
     'SECRET_KEY': '{ClientSecret}',
     'Debug':True,
     'OIDC_CLIENT_SECRETS': 'client_secrets.json',
     'OIDC_ID_TOKEN_COOKIE_SECURE': False,
     'OIDC_REQUIRE_VERIFIED_EMAIL': False,
     'OIDC_USER_INFO_ENABLED': True,
     'OIDC_OPENID_REALM': '{RealmName}',
     'OIDC_SCOPES': ['openid', 'email', 'profile'],
     'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})
8. Change only 'SECRET_KEY': '{ClientSecret}' and 'OIDC_OPENID_REALM': '{RealmName}',

# How To Run
1. Navigate to ..OIDC-Sample-Application-Python/OIDCSampleApplicationPython via python cmd
2. Type -->  python app.py
3. Application will Start running at some localhost port Ex: http://127.0.0.1:5000/
4. Copy the Url and Open it in Browser to Authenticate

# If Client is Public
1. If your Client is public, do not change the Client Secret.
2. ClientSecret will be ignored for public client
