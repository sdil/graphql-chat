import os

import stripe
from hasura_user_helper import set_stripe_id_hasura_user

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


def create_stripe_customer(firebase_id: str, email: str, name: str, metadata: dict):
    stripe_user = stripe.Customer.create(email=email, name=name, metadata=metadata)
    set_stripe_id_hasura_user(firebase_id, stripe_user.id)
    return True


def attach_payment_method_to_customer(customer: str, payment_method: str):
    stripe.PaymentMethod.attach(
        payment_method, customer=customer,
    )

def create_subscription(stripe_id: str, plan: str):
    # Get the price from Stripe
    # Assume Stripe as the source of truth for pricing
    price = None

    for product in stripe.Product.list(limit=50):
        price = stripe.Price.list(product=product.id)

    subscription = stripe.Subscription.create(
        customer=stripe_id,
        items=[{"price": price.data[0].id}]
    )

def set_default_payment_method(stripe_id: str, payment_method_id: str):
    stripe.Customer.modify(
        stripe_id,
        invoice_settings={
            'default_payment_method': payment_method_id,
        },
    )
