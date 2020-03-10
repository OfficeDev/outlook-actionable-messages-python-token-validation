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
 # Exemple Python de vérification du jeton de demande d’action

Les services peuvent envoyer des messages actionnables aux utilisateurs pour effectuer des tâches simples sur leurs services. Lorsqu’un utilisateur effectue l’une des actions dans un message, une demande d’action est envoyée au service par Microsoft. La demande de Microsoft contient un jeton du porteur dans l’en-tête d'autorisation. Cet exemple de code présente comment vérifier le jeton pour vous assurer que la demande d’action provient de Microsoft et utiliser les revendications dans le jeton pour valider la demande.

        @app.route("/api/dépense", methods = ["POST"])
        def api_post_expense():
            # Obtenir le jeton auprès de l'en-tête d’autorisation 
            
            autorisation = request.headers['Authorization']
            token_type, token = authorization.rsplit(' ', 1)
            
            if token_type.lower() != "porteur":
                abort(401)

            validateur = ActionableMessageTokenValidator()
            résultat = ActionableMessageTokenValidationResult()
            
            essayer :
                # Ceci valide l'émission du jeton par Microsoft pour le
                # l'URL cible spécifiée, autrement dit, la cible correspond à l’audience prévue (demande « aud » dans le jeton)
                # 
                # Dans votre code, remplacez https://api.contoso.com par l’URL de base de votre service.
                #/ Par exemple, si l’URL cible du service est https://api.xyz.com/finance/expense ?id=1234,
                # remplacez https://api.contoso.com par https://api.xyz.com
                
                résultat = validator.validate_token(token, "https://api.contoso.com")
            
            except InvalidActionableMessageTokenError as e:
                print(e)
                abort(401)
            
            # Un jeton valide existe. Vous allez maintenant vérifier que l’expéditeur et l'exécutant de l’action sont ceux
            # prévus. L’expéditeur correspond à l’identité de l’entité qui a initialement envoyé le Message 
            # actionnable et l’exécutant de l’action correspond à l’identité de l’utilisateur qui a réellement 
            # réalisé l’action (« sous- » revendication dans le jeton). 
            #
            # Vous devez remplacer le code ci-dessous par votre propre logique de validation. 
            # Dans cet exemple, vous vérifierez que le message électronique est envoyé par expense@contoso.com (expéditeur prévu)
            # et que l’adresse de courrier de la personne qui a effectué l’action est john@contoso.com (destinataire prévu)
            #
            # Vous devez également retourner l’en-tête CARD-ACTION-STATUS dans la réponse.
            # La valeur de l’en-tête s’affiche pour l’utilisateur.
            if result.sender.lower() != 'expense@contoso.com' or \
               result.action_performer.lower() != 'john@contoso.com'):
               resp = flask.Response('')
               resp.headers['CARD-ACTION-STATUS'] = 'Expéditeur non valide ou l'exécutant de l'action n'est pas autorisé.'
               return resp, 403

            # Code de logique métier plus précis ici pour traiter le rapport sur les dépenses.
            resp = flask.Response('')
            resp.headers['CARD-ACTION-STATUS'] = 'La dépense a été approuvée.'
            return resp

L’exemple de code utilise la bibliothèque suivante pour la validation JWT.   

[PyJWT](https://pypi.python.org/pypi/PyJWT/1.5.0)   

D'autres informations sur les Messages actionnables d'Outlook sont disponibles [ici](https://dev.outlook.com/actions).

## Copyright
Copyright (c) 2017 Microsoft. Tous droits réservés.


Ce projet a adopté le [code de conduite Open Source de Microsoft](https://opensource.microsoft.com/codeofconduct/). Pour en savoir plus, reportez-vous à la [FAQ relative au code de conduite](https://opensource.microsoft.com/codeofconduct/faq/) ou contactez [opencode@microsoft.com](mailto:opencode@microsoft.com) pour toute question ou tout commentaire.
