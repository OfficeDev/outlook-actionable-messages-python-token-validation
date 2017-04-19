# Action Request Token Verification Python Sample

Services can send actionable messages to users to complete simple tasks against their services. When a user performs one of the actions in a message, an action request will be sent by Microsoft to the service. The request from Microsoft will contain a bearer token in the authorization header. This code sample shows how to verify the token to ensure the action request is from Microsoft, and use the claims in the token to validate the request.

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

The code sample is using the following library for JWT validation.   

[PyJWT](https://pypi.python.org/pypi/PyJWT/1.5.0)   

More information Outlook Actionable Messages is available [here](https://dev.outlook.com/actions).

## Copyright
Copyright (c) 2017 Microsoft. All rights reserved.