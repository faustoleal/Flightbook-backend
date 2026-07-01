from pydantic import BaseModel

class LoginRequest(BaseModel):
  usuario: str
  password: str

class LoginResponse(BaseModel):
  token: str
  usuario: str
  id:int