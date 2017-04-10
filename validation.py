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
import binascii
import json
import jwt
import urllib.request

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from openid import OpenIDConnectConfiguration

class InvalidActionableMessageTokenError(Exception) : 
    pass
    
class ActionableMessageTokenValidationResult(object):
    def __init__(self):
        self.__sender = ''
        self.__action_performer = ''
        
    @property
    def sender(self):
        return self.__sender
        
    @sender.setter
    def sender(self, value):
        self.__sender = value
    
    @sender.deleter
    def sender(self):
        del self.__sender

    @property
    def action_performer(self):
        return self.__action_performer
        
    @action_performer.setter
    def action_performer(self, value):
        self.__action_performer = value
    
    @action_performer.deleter
    def action_performer(self):
        del self.__action_performer

class ActionableMessageTokenValidator(object):
    def __init__(self): pass
    
    def validation_token(self, token, targetUrl):
        try:
            result = ActionableMessageTokenValidationResult()
            openid_config = OpenIDConnectConfiguration('https://substrate.office.com/sts/common/.well-known/openid-configuration')
            signing_keys = openid_config.signing_keys()
            header = self._get_jwt_header(token)
            
            if header['kid'] not in signing_keys.keys():
                raise InvalidActionableMessageTokenError('KeyID {:s} does not exist'.format(header['kid']))
            
            public_key = signing_keys[header['kid']]
            
            claims = jwt.decode(
                token, 
                public_key, 
                algorithms=['RS256'], 
                issuer='https://substrate.office.com/sts/',
                audience=targetUrl)
            
            if claims['appid'].lower() != '48af08dc-f6d2-435f-b2a7-069abd99c086':
                raise InvalidActionableMessageTokenError('Invalid appid in the token')

            result.sender = claims['sender']
            result.action_performer = claims['sub']
        except Exception as e:
            raise InvalidActionableMessageTokenError('Validation failed: %s' % e)
            
        return result
        
    def _get_jwt_header(self, jwt):
        jwt = jwt.encode('utf-8')
        
        signing_input, crypto_segment = jwt.rsplit(b'.', 1)
        header_segment, payload_segment = signing_input.split(b'.', 1)
        header_data = base64.urlsafe_b64decode(header_segment)
        header = json.loads(header_data.decode('utf-8'))
        
        return header
