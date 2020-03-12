---
page_type: sample
products:
- office-outlook
- office-365
languages:
- python
extensions:
  contentType: samples
  technologies:
  - Actionable messages
  createdDate: 11/17/2016 2:43:33 PM
---
 # アクション要求トークンの検証 Python サンプル

サービスは、アクション可能メッセージをユーザーに送信して、サービスに対する単純なタスクを完了することができます。ユーザーがメッセージに含まれるいずれかのアクションを実行すると、Microsoft によりアクション要求がサービスに対して送信されます。Microsoft からの要求には、認証ヘッダーにベアラー トークンが含まれています。このコード サンプルでは、トークンを検証して、アクション要求が Microsoft からのものであることを確認し、トークンの要求を使用して要求を検証する方法を示します。

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
            
            # We have a valid token.We will now verify that the sender and action performer are who
            # we expect.The sender is the identity of the entity that initially sent the Actionable 
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

このコード サンプルでは、JWT 認証に次のライブラリを使用しています。   

[PyJWT](https://pypi.python.org/pypi/PyJWT/1.5.0)   

Outlook のアクション可能メッセージの詳細については、[こちら](https://dev.outlook.com/actions)をクリックしてください。

## 著作権
Copyright (c) 2017 Microsoft.All rights reserved.


このプロジェクトでは、[Microsoft オープン ソース倫理規定](https://opensource.microsoft.com/codeofconduct/)が採用されています。詳細については、「[倫理規定の FAQ](https://opensource.microsoft.com/codeofconduct/faq/)」を参照してください。また、その他の質問やコメントがあれば、[opencode@microsoft.com](mailto:opencode@microsoft.com) までお問い合わせください。
