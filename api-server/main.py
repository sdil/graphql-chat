from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from hasura_user_helper import get_user, create_user
import pyrebase
import urllib.error
import os

# FastAPI setup
app = FastAPI()
security = HTTPBearer()


# Firebase setup
config = {
    "apiKey": os.environ.get("APIKEY"),
    "authDomain": "",
    "databaseURL": "",
    "storageBucket": "",
    "serviceAccount": "service-account.json",
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.get("/healthz")
def healthz():
    """
    Health check
    """
    return {"status": "OK"}


@app.get("/get-or-create-user")
def get_or_create_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify the user token in Authorization request header.
    If the token is valid, get user info if exist in DB
    If the user is not exists, create a new record in DB
    """
    token = credentials.credentials

    try:
        user = auth.get_account_info(token)["users"][0]
    except Exception as e:
        return {"message": f"Invalid authentication credentials", "error": str(e)}

    # At this point, Firebase Auth already verified the user is valid.
    # Get the user in DB from Hasura to check whether it's already in DB
    # If the user not in DB yet, creates the new user record in DB
    # If the user already exists, do nothing.
    # This is an idempotent operation.
    try:
        user = get_user(user["localId"])
    except urllib.error.URLError:
        return {"message": f"Failed to connect to Chat auth server"}

    if not user:
        create_user(user)
        return {"message": f"New user '{user}' is created"}

    return {"message": f"User '{user['email']}' is already exists"}
