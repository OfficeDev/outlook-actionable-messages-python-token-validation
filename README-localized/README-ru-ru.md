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
 # Пример кода Python для проверки маркера запроса

Службы могут отправлять пользователям интерактивные сообщения для выполнения простых задач в отношении своих служб. При выполнении пользователем одного из действий в сообщении, ему будет отправлен запрос на обслуживание от Майкрософт. Запрос от Майкрософт будет содержать маркер носителя в заголовке авторизации. В этом примере кода показано, как проверить маркер, чтобы убедиться, что запрос получен от Майкрософт, и использовать утверждения в маркере для проверки запроса.

        @app.route("/api/expense", methods = ["POST"])
        def api_post_expense():
            # Получить маркер из заголовка авторизации 
            
            authorization = request.headers['Authorization']
            token_type, token = authorization.rsplit(' ', 1)
            
            if token_type.lower() != "bearer":
                abort(401)

            validator = ActionableMessageTokenValidator()
            result = ActionableMessageTokenValidationResult()
            
            try:
                # Данное действие подтверждает, что маркер был выдан корпорацией Майкрософт
                # для указанного конечного URL-адреса, т. е. цель совпадает с целевой аудиторией (утверждение "aud" в маркере)
                # 
                # Замените в вашем коде https://api.contoso.com на базовый URL-адрес вашей службы.
                # Например, если целевой URL-адрес службы — https://api.xyz.com/finance/expense?id=1234,
                # замените https://api.contoso.com на https://api.xyz.com
                
                result = validator.validate_token(token, "https://api.contoso.com")
            
            Кроме InvalidActionableMessageTokenError в виде e:
                печать (e)
                abort(401)
            
            # У нас действительный маркер. Теперь нужно убедиться, что отправитель и исполнитель действия являются теми,
            # кого мы ожидаем. Отправитель — это идентификация субъекта, который изначально отправил интерактивное 
            # сообщение, а исполнитель действия — это идентификация пользователя, который в действительности 
            # выполнил действие (утверждение "sub" в маркере). 
            #
            # Вам потребуется заменить указанный ниже код на собственную логику проверки 
            # В этом примере мы проверяем, что сообщение отправлено expense@contoso.com (ожидаемый отправитель)
            # и электронная почта лица, выполнившего действие, — john@contoso.com (ожидаемый получатель)
            #
            # Вам потребуется также вернуть заголовок CARD-ACTION-STATUS в ответе.
            # Значение заголовка будет отображаться для пользователя.
            if result.sender.lower() != 'expense@contoso.com' or \
               result.action_performer.lower() != 'john@contoso.com'):
               resp = flask.Response('')
               resp.headers['CARD-ACTION-STATUS'] = 'Invalid sender or the action performer is not allowed.'
               return resp, 403

            # Дальнейший представленный здесь код бизнес-логики предназначен для обработки отчета о расходах.
            resp = flask.Response('')
            resp.headers['CARD-ACTION-STATUS'] = 'The expense was approved.'
            return resp

Образец кода использует следующую библиотеку для проверки JWT.   

[PyJWT](https://pypi.python.org/pypi/PyJWT/1.5.0)   

Дополнительные сведения об интерактивных сообщениях в Outlook доступны [здесь](https://dev.outlook.com/actions).

## Авторские права
(c) Корпорация Майкрософт (Microsoft Corporation), 2017. Все права защищены.


Этот проект соответствует [Правилам поведения разработчиков открытого кода Майкрософт](https://opensource.microsoft.com/codeofconduct/). Дополнительные сведения см. в разделе [часто задаваемых вопросов о правилах поведения](https://opensource.microsoft.com/codeofconduct/faq/). Если у вас возникли вопросы или замечания, напишите нам по адресу [opencode@microsoft.com](mailto:opencode@microsoft.com).
