from foqus.cloud_configuration import *
import datetime
import time
import stripe


def create_stripe_customer(ident, email, source):
    """ Create ``stripe.Customer`` with a source.
    NB: doesn't check for customer existence.
    :param ident: str to use for the stripe Customer
    :param email: str user email
    :param source: source arg for stripe (going to be a token for our usage)
    :return: stripe.Customer new
    """
    cust = stripe.Customer.create(
        id=ident, email=email, source=source)
    return cust


def update_stripe_customer_source(customer, new_source):
    """ Set the new source as the unique new source for this customer.
    This is not optimal in terms of using the Stripe API, but it's easier to
    maintain and think about.
    NB: Raises if Customer doesn't exist.
    :param customer: stripe.Customer
    :param new_source: stripe source arg
    :return: stripe.Customer updated
    """
    try:
        card = customer.sources.create(source=new_source)
        for old_card in (c for c in customer.sources.data if c.id != card.id):
            old_card.delete()
    except Exception as e:
        logger.error("------------->>>>>>>>>> error %s" %e)
    return customer


def charge_stripe_customer_id(customer_id, currency, amount_in_cents, description, order_id):
    """
    :param customer_id: stripe customer id
    :param amout_in_cents: int
    :param description: charge description
    :return: stripe.Charge new
    """
    return stripe.Charge.create(
        customer=customer_id,
        currency=currency,
        amount=amount_in_cents,
        description=description,
        metadata={'order_id': '%s' % order_id}
    )


def subscribe_stripe_customer(customer, stripe_plan):
    """
    Start subscriptions to the corresponding stripe plan with a trial period
    exactly equal to the plan delta between two payments.
    The first payment corresponding to the plan should have been done in a
    separated one-time charge.
    If the stripe plan is not defined or equal to zero we force the trial period to be equal
    one interval.
    Otherwise we just use the trial period value.
    :param customer: stripe.Customer
    :param stripe_plan: payments.models.StripePlan
    :return: stripe.Subscription new
    """
    date = datetime.datetime.today()
    date_month = int(date.strftime("%m"))
    next_payement_date = date.replace(month=date_month + 1 if date_month < 12 else 1).strftime("%Y-%m-%d")
    next_payement_timestamp = int(time.mktime(datetime.datetime.strptime(next_payement_date, "%Y-%m-%d").timetuple()))

    try:
        stripe.Subscription.create(
            customer=customer,
            items=[
                {
                "plan": "foqus_%s" % stripe_plan,
                }
            ],
            trial_end=next_payement_timestamp
                    )
    except Exception as e:
        logger.info('-------------- %s -------------' %e)


def create_plan_stripe(name, price, currency):
            strip_plan = stripe.Plan.create(
                amount=int(price * 100),
                interval_count=1,
                trial_period=None,
                id='foqus_%s' %name,
                currency=currency,
                interval='year',
                name=name
            )