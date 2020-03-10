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
 # Ejemplo de comprobación de token de solicitud de acción en Python

Los servicios pueden enviar mensajes accionables a los usuarios para que realicen tareas sencillas en sus servicios. Cuando un usuario realiza una de las acciones de un mensaje, Microsoft enviará una solicitud de acción al servicio. La solicitud de Microsoft contendrá un token de portador en el encabezado de la autorización. En este ejemplo de código se muestra cómo comprobar el token para garantizar que la solicitud de acción es de Microsoft, y usar las notificaciones del token para validar la solicitud.

        @app.route("/api/expense", methods = ["POST"])
        def api_post_expense():
            # Obtener el token del encabezado de autorización 
            
            authorization = request.headers['Authorization']
            token_type, token = authorization.rsplit(' ', 1)
            
            if token_type.lower() != "bearer":
                abort(401)

            validator = ActionableMessageTokenValidator()
            result = ActionableMessageTokenValidationResult()
            
            probar:
                # Esto validará que el token fue emitido por Microsoft para la
                # dirección URL de destino especificada, es decir, el destino coincide con el público deseado (notificación "aud" de token)
                # 
                # En su código, reemplace https://api.contoso.com por la dirección URL base del servicio.
                # Por ejemplo, si la dirección URL del servicio de destino es https://api.xyz.com/finance/expense?id=1234,
                # reemplace https://api.contoso.com por https://api.xyz.com
                
                result = validator.validate_token(token, "https://api.contoso.com")
            
            except InvalidActionableMessageTokenError as e:
                print(e)
                abort(401)
            
            # Ya tenemos un token válido. Ahora verificaremos que el remitente y el ejecutante de la acción sean quiénes
            # esperamos. El remitente es la identidad de la entidad que envió inicialmente el mensaje 
            # que requiere acción, y el ejecutante de la acción es la identidad del usuario que realmente 
            # realizó la acción (notificación "sub" de token) 
            #
            # Debería reemplazar el código siguiente con su propia lógica de validación 
            # En este ejemplo, comprobamos que el correo electrónico es enviado por expense@contoso.com (remitente esperado)
            # y el correo electrónico de la persona que realizó la acción es john@contoso.com (destinatario esperado)
            #
            # También debería devolver el encabezado CARD-ACTION-STATUS en la respuesta.
            # El valor del encabezado se mostrará al usuario.
            if result.sender.lower() != 'expense@contoso.com' or \
               result.action_performer.lower() != 'john@contoso.com'):
               resp = flask.Response('')
               resp.headers['CARD-ACTION-STATUS'] = 'Remitente no válido o no se permite el ejecutante de la acción.'
               return resp, 403

            # Código de lógica empresarial adicional para procesar el informe de gastos.
            resp = flask.Response('')
            resp.headers['CARD-ACTION-STATUS'] = 'Se ha aprobado el gasto.'
            return resp

El código de ejemplo usa la siguiente biblioteca para la validación de JWT.   

[PyJWT](https://pypi.python.org/pypi/PyJWT/1.5.0)   

Puede encontrar más información sobre los mensajes accionables de Outlook [aquí](https://dev.outlook.com/actions).

## Derechos de autor
Copyright (c) 2017 Microsoft. Todos los derechos reservados.


Este proyecto ha adoptado el [Código de conducta de código abierto de Microsoft](https://opensource.microsoft.com/codeofconduct/). Para obtener más información, vea [Preguntas frecuentes sobre el código de conducta](https://opensource.microsoft.com/codeofconduct/faq/) o póngase en contacto con [opencode@microsoft.com](mailto:opencode@microsoft.com) si tiene otras preguntas o comentarios.
