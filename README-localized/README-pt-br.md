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
 # Exemplo em Python de verificação de token de solicitação de ação

Serviços podem enviar mensagens acionáveis para usuários para que os mesmos completem tarefas simples em oposição aos seus serviços. Quando um usuário executar uma das ações em uma mensagem, uma solicitação de ação será enviada pela Microsoft para o serviço. A solicitação da Microsoft conterá um token de portador no cabeçalho de autorização. Este exemplo de código mostra como verificar o token para garantir que a solicitação de ação veio mesmo da Microsoft e como usar as declarações do token para validar a solicitação.

        @app.route("/api/expense", methods = ["POST"])
        def api_post_expense():
            # Solicite um novo token do servidor de autorização. 
            
            autorização = solicitação headers ['Autorização']
            token_type, token = authorization.rsplit(' ', 1)
            
            if token_type.lower() != "bearer":
                abort(401)

            validator = ActionableMessageTokenValidator()
            result = ActionableMessageTokenValidationResult()
            
            tentar:
                # Isto verificará se o token foi emitido pela Microsoft para o
                # URL de destino especificada, ou seja, o destino corresponde à audiência desejada (declaração de "AUD" no token)
                # 
                # Em seu código, substitua https://api.contoso.com pela URL base do seu serviço.
                # Por exemplo, se a URL de destino do serviço for https://api.xyz.com/finance/expense?id=1234,
                # em seguida, substitua https://api.contoso.com por https://api.xyz.com
                
                result = validator.validate_token(token, "https://api.contoso.com")
            
            exceto InvalidActionableMessageTokenError como e:
                print(e)
                abort(401)
            
            # Temos um token válido. Agora, verificaremos se o remetente e a ação executores são quem
            # Esperamos. O remetente é a identidade da entidade que enviou a ação 
            # Mensagem, e o executor da ação é a identidade do usuário que 
            # tomou a ação ("sub" declaração no token). 
            #
            # Você deve substituir o código abaixo por sua própria lógica de validação 
            # Neste exemplo, verificamos se o email foi enviado por expense@contoso.com (remetente esperado)
            # e o email da pessoa que executou a ação é john@contoso.com (destinatário esperado)
            #
            # Você também deve retornar o cabeçalho do STATUS da ação de cartão na resposta.
            # O valor do cabeçalho será exibido para o usuário.
            se result.sender.lower() != 'expense@contoso.com' or \
               result.action_performer.lower() != 'john@contoso.com'):
               resp = flask.Response('')
               resp.headers [' CARD-ACTION-STATUS '] = ' remetente inválido ou o executor da ação não é permitido. '
               retornar resp, 403

            # Outro código de lógica de negócios aqui para processar o relatório de despesas.
            resp = flask.Response('')
            resp.headers [' CARD-ACTION-STATUS '] = ' a despesa foi aprovada. '
            retornar resp

O exemplo de código está usando a biblioteca a seguir para a validação de JWT.   

[PyJWT](https://pypi.python.org/pypi/PyJWT/1.5.0)   

Mais informações as Mensagens Acionáveis do Outlook estão disponíveis](https://dev.outlook.com/actions)aqui](https://dev.outlook.com/actions).

## Direitos autorais
Copyright (c) 2017 Microsoft. Todos os direitos reservados.


Este projeto adotou o [Código de Conduta do Código Aberto da Microsoft](https://opensource.microsoft.com/codeofconduct/). Para saber mais, confira [Perguntas frequentes sobre o Código de Conduta](https://opensource.microsoft.com/codeofconduct/faq/) ou contate [opencode@microsoft.com](mailto:opencode@microsoft.com) se tiver outras dúvidas ou comentários.
