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

import base64
import binascii
import json
import jwt
import urllib.request

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from openid import OpenIDConnectConfiguration

class InvalidActionableMessageTokenError(Exception) : 
    """
    Represents the error where the actionable message token is invalid.
    """
    pass
    
class ActionableMessageTokenValidationResult(object):
    """
    Result from a token validation.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        self.__sender = ''
        self.__action_performer = ''

    @property
    def sender(self):
        """
        Gets the sender.
        """
        return self.__sender
        
    @sender.setter
    def sender(self, value):
        """
        Sets the sender.
        """
        self.__sender = value
    
    @sender.deleter
    def sender(self):
        """
        Deletes the sender property.
        """
        del self.__sender

    @property
    def action_performer(self):
        """
        Gets the action performer.
        """
        return self.__action_performer
        
    @action_performer.setter
    def action_performer(self, value):
        """
        Sets the action performer.
        """
        self.__action_performer = value
    
    @action_performer.deleter
    def action_performer(self):
        """
        Deletes the action performer property.
        """
        del self.__action_performer

class O365OpenIdConfiguration(object):
    """
    Constants for O365 Open ID configuration.
    """
    APP_ID = "48af08dc-f6d2-435f-b2a7-069abd99c086";
    METADATA_URL = "https://substrate.office.com/sts/common/.well-known/openid-configuration";
    TOKEN_ISSUER = "https://substrate.office.com/sts/";
        
class ActionableMessageTokenValidator(object):
    """
    The validator for actionable message token.
    """
    
    def __init__(self): 
        """
        Constructor.
        """
        pass
    
    def validate_token(self, token, targetUrl):
        """
        Validate the JWT token issued by Microsoft.
        """
        try:
            result = ActionableMessageTokenValidationResult()
            openid_config = OpenIDConnectConfiguration(O365OpenIdConfiguration.METADATA_URL)
            header = self._get_jwt_header(token)
            public_key = openid_config.get_key(header['kid'])
            
            if public_key is None:
                raise InvalidActionableMessageTokenError('KeyID {:s} does not exist'.format(header['kid']))
            
            claims = jwt.decode(
                token, 
                public_key, 
                algorithms=['RS256'], 
                issuer=O365OpenIdConfiguration.TOKEN_ISSUER,
                audience=targetUrl)
            
            if claims['appid'].lower() != O365OpenIdConfiguration.APP_ID:
                raise InvalidActionableMessageTokenError('Invalid appid in the token')

            result.sender = claims['sender']
            result.action_performer = claims['sub']
        except Exception as e:
            raise InvalidActionableMessageTokenError('Validation failed: %s' % e)
            
        return result
        
    def _get_jwt_header(self, jwt):
        """
        Gets the header of the JWT token.
        """
        jwt = jwt.encode('utf-8')
        
        signing_input, crypto_segment = jwt.rsplit(b'.', 1)
        header_segment, payload_segment = signing_input.split(b'.', 1)
        header_data = base64.urlsafe_b64decode(header_segment)
        header = json.loads(header_data.decode('utf-8'))
        
        return header
