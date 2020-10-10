from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()
security = HTTPBearer()


@app.get("/healthz")
def healthz():
    return {"status": "OK"}


@app.get("/get-or-create-user")
def get_or_create_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}
