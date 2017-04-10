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
        print("bearer token not found")
        abort(500)

    validator = ActionableMessageTokenValidator()
    result = ActionableMessageTokenValidationResult()
    
    try:
        # Replace [WEB SERVICE URL] with your service domain URL.
        # For example, if the service URL is https://api.contoso.com/finance/expense?id=1234,
        # then replace [WEB SERVICE URL] with https://api.contoso.com
        result = validator.validation_token(token, "[WEB SERVICE URL]")
    
    except InvalidActionableMessageTokenError as e:
        print(e)
        abort(500)
    
    # We have a valid token. We will verify the sender and the action performer. 
    # In this example, we verify that the email is sent by Contoso LOB system
    # and the action performer has to be someone with @contoso.com email.
    if result.sender.lower() != 'lob@contoso.com' or \
       not result.action_performer.lower().endswith('@contoso.com'):
       print('Invalid sender or the action performer is not allowed.')
       abort(500)
    
    return ''

if __name__ == "__main__":
    app.run();
