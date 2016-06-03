#!/usr/bin/env python
# Module to get access or refresh token from Reddit's authentication server (OAuth2)
import webbrowser
import sys
import praw
import api_auth

## USER AUTHENTICATION & API ACCESS ##
r = api_auth.get_info()

if len(sys.argv) == 1:
    print "Getting access token..."
    url = r.get_authorize_url('uniqueKey', 'identity edit submit read', True)
    webbrowser.open(url) # Take code from here and paste as 'token'
    print "Copy token from 'code' parameter in url and pass as parameter to this program i.e. ./get_token.py [token]"
elif len(sys.argv) == 2:
    print "Getting refresh token..."
    token = sys.argv[1]
    access_info = r.get_access_information(token)
    refresh_token = access_info['refresh_token']
    print "Refresh token: ", refresh_token
    f = open("token.txt", "w")
    f.write(refresh_token)
    f.close()
else:
    print "Usage: ./get_token.pyy || ./get_token.py [token]"
