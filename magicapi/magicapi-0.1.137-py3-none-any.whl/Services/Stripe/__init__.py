import stripe
from magicapi import g

if g.settings.stripe_env == "production":
    stripe.api_key = g.settings.stripe_api_key_production
else:
    stripe.api_key = g.settings.stripe_api_key_sandbox
