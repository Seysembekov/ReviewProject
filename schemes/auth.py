from pydantic import BaseModel, field_validator, Field
import re

class RegisterData(BaseModel):
    username: str
    password: str

    @field_validator('password')
    @classmethod
    def strong(cls, v):
        if not re.search(r'[A-Za-z]', v) or not re.search(r'\d', v):
            raise ValueError('Weak password')
        return v
class LoginData(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'