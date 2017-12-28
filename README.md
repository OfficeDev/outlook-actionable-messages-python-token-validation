 # Action Request Token Verification Python Sample

Services can send actionable messages to users to complete simple tasks against their services. When a user performs one of the actions in a message, an action request will be sent by Microsoft to the service. The request from Microsoft will contain a bearer token in the authorization header. This code sample shows how to verify the token to ensure the action request is from Microsoft, and use the claims in the token to validate the request.

        @app.route("/api/expense", methods = ["POST"])
        def api_post_expense():
            # Get the token from the Authorization header 
            
            authorization = request.headers['Authorization']
            token_type, token = authorization.rsplit(' ', 1)
            
            if token_type.lower() != "bearer":
                abort(401)

            validator = ActionableMessageTokenValidator()
            result = ActionableMessageTokenValidationResult()
            
            try:
                # This will validate that the token has been issued by Microsoft for the
                # specified target URL i.e. the target matches the intended audience (“aud” claim in token)
                # 
                # In your code, replace https://api.contoso.com with your service’s base URL.
                # For example, if the service target URL is https://api.xyz.com/finance/expense?id=1234,
                # then replace https://api.contoso.com with https://api.xyz.com
                
                result = validator.validate_token(token, "https://api.contoso.com")
            
            except InvalidActionableMessageTokenError as e:
                print(e)
                abort(401)
            
            # We have a valid token. We will now verify that the sender and action performer are who
            # we expect. The sender is the identity of the entity that initially sent the Actionable 
            # Message, and the action performer is the identity of the user who actually 
            # took the action (“sub” claim in token). 
            #
            # You should replace the code below with your own validation logic 
            # In this example, we verify that the email is sent by expense@contoso.com (expected sender)
            # and the email of the person who performed the action is john@contoso.com (expected recipient)
            #
            # You should also return the CARD-ACTION-STATUS header in the response.
            # The value of the header will be displayed to the user.
            if result.sender.lower() != 'expense@contoso.com' or \
               result.action_performer.lower() != 'john@contoso.com'):
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


This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
