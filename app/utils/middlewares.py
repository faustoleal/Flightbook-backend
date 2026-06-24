from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request

class TokenExtractor(BaseHTTPMiddleware):
 async def dispatch(self,request:Request, call_next):
   authorization: str | None = request.headers.get("authorization")
   if authorization and authorization.startswith("Bearer "):
    request.state.token = authorization[7:]
   else:
    request.state.token = None
  
   response = await call_next(request)
   return response