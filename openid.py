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
import datetime
import json
import urllib.request

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import (datetime, timedelta)

class OpenIDConnectConfiguration(object):
    """
    Represents an OpenID configuration.
    """
    
    lastUpdated = datetime.now()
    signing_keys = {}

    def __init__(self, url):
        """
        Construtor.
        """
        self._url = url
        keys = OpenIDConnectConfiguration.signing_keys.get(url)
        if keys is None:
            OpenIDConnectConfiguration.refresh_cache(url)

    def get_key(self, keyId):
        """
        Gets the public key from the cache given the key ID.
        """
        diff = datetime.now() - OpenIDConnectConfiguration.lastUpdated

        # Refresh the cache if it's more than 5 days old.
        if diff.total_seconds() > 5 * 24 * 60 * 60:
            refresh_cache()

        keys  = OpenIDConnectConfiguration.signing_keys.get(self._url)
        if keys is not None:
            return keys.get(keyId)
            
        return None

    @staticmethod
    def refresh_cache(url):
        """
        Refresh the keys cache.
        """
        openid_config = OpenIDConnectConfiguration.load_config(url)
        jwks_uri = openid_config['jwks_uri']
        keys = OpenIDConnectConfiguration.load_jwks(jwks_uri)
        
        OpenIDConnectConfiguration.signing_keys[url] = keys

    @staticmethod
    def load_config(url):
        """
        Load the Open ID configuration from the given URL.
        """
        req = urllib.request.urlopen(url)
        openid_config = json.loads(req.read().decode('utf-8'))
        
        return openid_config
        # jwks_uri = openid_config['jwks_uri']
        # self.load_jwks(jwks_uri)
    
    @staticmethod
    def load_jwks(url):
        """
        Loads the JSON web key set from the given URL.
        """
        req = urllib.request.urlopen(url)
        jwks = json.loads(req.read().decode('utf-8'))
        keys = {}
        
        for key in jwks['keys']:
            exp_b64 = key['e']
            modulus_b64 = key['n']
            exp = int(binascii.hexlify(base64.urlsafe_b64decode(pad_base64_str(exp_b64))), 16)
            mod = int(binascii.hexlify(base64.urlsafe_b64decode(pad_base64_str(modulus_b64))), 16)
            pub_num = rsa.RSAPublicNumbers(exp, mod)
            public_key = pub_num.public_key(default_backend())
            keys[key['kid']] = public_key
        
        return keys
        
def pad_base64_str(str):
    """
    Pads the base64 string.
    """
    missing_padding = len(str) % 4
    if missing_padding != 0:
        str += '=' * (4 - missing_padding)
    return str
