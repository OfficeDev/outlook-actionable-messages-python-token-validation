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
import urllib.request

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

class OpenIDConnectConfiguration(object):
    def __init__(self, url):
        self.load_config(url)
    
    def load_config(self, url):
        req = urllib.request.urlopen(url)
        openid_config = json.loads(req.read().decode('utf-8'))
        jwks_uri = openid_config['jwks_uri']
        self.load_jwks(jwks_uri)
    
    def load_jwks(self, url):
        req = urllib.request.urlopen(url)
        jwks = json.loads(req.read().decode('utf-8'))
        self._signing_keys = {}
        
        for key in jwks['keys']:
            exp_b64 = key['e']
            modulus_b64 = key['n']
            exp = int(binascii.hexlify(base64.urlsafe_b64decode(pad_base64_str(exp_b64))), 16)
            mod = int(binascii.hexlify(base64.urlsafe_b64decode(pad_base64_str(modulus_b64))), 16)
            pub_num = rsa.RSAPublicNumbers(exp, mod)
            public_key = pub_num.public_key(default_backend())
            self._signing_keys[key['kid']] = public_key
        
    def signing_keys(self):
        return self._signing_keys

def pad_base64_str(str):
    missing_padding = len(str) % 4
    if missing_padding != 0:
        str += '=' * (4 - missing_padding)
    return str
