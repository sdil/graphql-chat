import os

import stripe
from hasura_user_helper import set_stripe_id_hasura_user

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


def create_stripe_customer(firebase_id:str, email: str, name: str, metadata: dict):
    stripe_user = stripe.Customer.create(email=email, name=name, metadata=metadata)
    set_stripe_id_hasura_user(firebase_id, stripe_user.id)
    return True
