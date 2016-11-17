# 
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.
# 
# Copyright (c) Microsoft Corporation
# All rights reserved.
# 
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import base64
import json
import jwt

from cryptography.hazmat.backends import default_backend
from flask import Flask, request, abort
from openid import OpenIDConnectConfiguration

app = Flask(__name__)

@app.route("/api/expense", methods = ["POST"])
def api_post_expense():
    openid_config = OpenIDConnectConfiguration('https://substrate.office.com/sts/common/.well-known/openid-configuration')
    
    authorization = request.headers['Authorization']
    token_type, token = authorization.rsplit(' ', 1)
    
    if token_type.lower() != "bearer":
        print("bearer token not found")
        abort(500)

    signing_keys = openid_config.signing_keys()
    header = get_jwt_header(token)
    
    if header['kid'] not in signing_keys.keys():
        print('KeyID {:s} does not exist'.format(header['kid']))
        abort(500)
    
    public_key = signing_keys[header['kid']]
    
    # Replace [WEB SERVICE URL] with your service domain URL.
    # For example, if the service URL is https://api.contoso.com/finance/expense?id=1234,
    # then replace [WEB SERVICE URL] with https://api.contoso.com
    claims = jwt.decode(
        token, 
        public_key, 
        algorithms=['RS256'], 
        issuer='https://substrate.office.com/sts/',
        audience='[WEB SERVICE URL]')
    
    if claims['appid'].lower() != '48af08dc-f6d2-435f-b2a7-069abd99c086':
        abort(500)
    
    # sender claim will contain the email address of the sender.
    # Validate that the email is sent by your organization.
    sender = claims['sender']
    
    # subject claim will contain the email of the person who performed the action.
    # Validate that the person has the priviledge to perform this action.
    subject = claims['sub']
    
    return ''

def get_jwt_header(jwt):
    jwt = jwt.encode('utf-8')
    
    signing_input, crypto_segment = jwt.rsplit(b'.', 1)
    header_segment, payload_segment = signing_input.split(b'.', 1)
    header_data = base64.urlsafe_b64decode(header_segment)
    header = json.loads(header_data.decode('utf-8'))
    
    return header
    
if __name__ == "__main__":
    app.run();
