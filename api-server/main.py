import logging
import os
import urllib.error

import pyrebase
from fastapi import FastAPI, Security
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from hasura_user_helper import create_hasura_user, get_hasura_user
from stripe_helper import create_stripe_customer

# Configure the root log level and ensure all logs are sent to Gunicorn's error log.
gunicorn_error_logger = logging.getLogger("gunicorn.error")
# (you could probably just use = instead extend below)
logging.root.handlers.extend(gunicorn_error_logger.handlers)
logging.root.setLevel(gunicorn_error_logger.level)


# FastAPI setup
app = FastAPI()
security = HTTPBearer()

origins = [
    "http://localhost:3000",
    "https://chat.fadhil-blog.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Firebase setup
config = {
    "apiKey": os.environ.get("FIREBASE_API_KEY"),
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
    return JSONResponse({"status": "OK"})


@app.get("/get-or-create-user")
def get_or_create_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify the user token in Authorization request header.
    If the token is valid, get user info if exist in DB
    If the user is not exists, create a new record in DB
    """
    token = credentials.credentials

    logger.info(token)

    try:
        firebase_user = auth.get_account_info(token)["users"][0]
    except Exception as e:
        logger.info(f"Failed to connect to Firebase server. Error msg: {e}")
        return JSONResponse(
            {"message": f"Invalid authentication credentials", "error": str(e)}
        )

    # At this point, Firebase Auth already verified the user is valid.
    # Get the user in DB from Hasura to check whether it's already in DB
    # If the user not in DB yet, creates the new user record in DB
    # If the user already exists, do nothing.
    # This is an idempotent operation.
    try:
        hasura_user = get_hasura_user(firebase_user["localId"])
    except urllib.error.URLError:
        logger.info(f"Failed to connect to Hasura")
        return JSONResponse({"message": f"Failed to connect to Chat auth server"})

    if not hasura_user:
        try:
            create_hasura_user(firebase_user)
            logger.info(f"Hasura user '{firebase_user['displayName']}' is created")
            create_stripe_customer(
                firebase_user["localId"],
                firebase_user["email"],
                firebase_user["displayName"],
                {"id": firebase_user["localId"]},
            )
            logger.info(f"Stripe customer '{firebase_user['displayName']}' is created")
            return JSONResponse({"message": f"New user '{firebase_user}' is created"})

        except Exception as e:
            logger.info(f"Failed to create new user '{firebase_user['displayName']}'. Error message: {e}")
            return JSONResponse({"message": f"Failed to create new user '{firebase_user}'"})

    logger.info(f"User '{user['name']}' is already exists")
    return JSONResponse(
        {"message": f"User '{firebase_user['displayName']}' is already exists"}
    )


@app.get("/create-payment-intent")
def create_payment_intent():
    """
    Always calculate the order amount on your server to prevent customers
    from manipulating the order amount from the client
    Here we will use a simple json file to represent inventory
    but you could replace this with a DB lookup
    """
    payment_intent = stripe.PaymentIntent.create(amount=2000, currency="usd")
    return JSONResponse({"clientSecret": payment_intent.client_secret})
