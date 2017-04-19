# 
# Copyright (c) Microsoft Corporation.
# All rights reserved.
# 
# This code is licensed under the MIT License.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions :
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

import flask

from flask import Flask, request, abort
from validation import (
    InvalidActionableMessageTokenError,
    ActionableMessageTokenValidator,
    ActionableMessageTokenValidationResult
)

app = Flask(__name__)

@app.route("/api/expense", methods = ["POST"])
def api_post_expense():
    authorization = request.headers['Authorization']
    token_type, token = authorization.rsplit(' ', 1)
    
    if token_type.lower() != "bearer":
        abort(401)

    validator = ActionableMessageTokenValidator()
    result = ActionableMessageTokenValidationResult()
    
    try:
        # validate_token will verify the following
        # 1. The token is issued by Microsoft and its digital signature is valid.
        # 2. The token has not expired.
        # 3. The audience claim matches the service domain URL.
        #
        # Replace https://api.contoso.com with your service domain URL.
        # For example, if the service URL is https://api.xyz.com/finance/expense?id=1234,
        # then replace https://api.contoso.com with https://api.xyz.com
        result = validator.validate_token(token, "https://api.contoso.com")
    
    except InvalidActionableMessageTokenError as e:
        print(e)
        abort(401)
    
    # We have a valid token. We will verify the sender and the action performer. 
    # You should replace the code below with your own validation logic.
    # In this example, we verify that the email is sent by expense@contoso.com
    # and the action performer has to be someone with @contoso.com email.
    #
    # You should also return the CARD-ACTION-STATUS header in the response.
    # The value of the header will be displayed to the user.
    if result.sender.lower() != 'expense@contoso.com' or \
       not result.action_performer.lower().endswith('@contoso.com'):
       resp = flask.Response('')
       resp.headers['CARD-ACTION-STATUS'] = 'Invalid sender or the action performer is not allowed.'
       return resp, 403

    # Further business logic code here to process the expense report.
    resp = flask.Response('')
    resp.headers['CARD-ACTION-STATUS'] = 'The expense was approved.'
    return resp

if __name__ == "__main__":
    app.run();
