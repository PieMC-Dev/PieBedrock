import jwt

class JWT:
    
    def __init__(self, secret, algorithm="HS256"):
        self.secret = secret
        self.algorithm = algorithm

    def encode(self, payload):
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return token

    def decode(self, token):
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        return payload
