from foqus.stripe_payment import *

stripe.api_key = STRIPE_SKEY


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


def generate_transaction_id(payement):
    import random, string
    """ Generates a charge_id """
    transaction_id = '%s_%s_%s' % (
        payement.payment_method,
        payement.pk,
        ''.join(random.choice(string.digits) for _ in range(10)))
    return transaction_id


def generate_stripe_customer_id(payment, token, email):
    """ If no ``stripe_customer_id``, create a Stripe customer with the
    given token as srouce.
    Else, update with the token:
        - if no card present, add the new card
        - if any number of cards already present, add the new card and
        remove all the older cards
    Raises stripe errors if problems with the card or the API.
    :param token: stripe.js token
    :return: stripe.Customer, bool created?
    """
    created = False

    stripe_customer_id = 'client_foqus_payment__%s' % (payment[0])
    try:
        cust = create_stripe_customer(
            stripe_customer_id,
            email,
            token)
        logger.info('->RIP<- %s' % cust)
        stripe_customer_id = cust.id
        created = True
    except Exception as e:
        stripe_customer_id = stripe_customer_id
        logger.info(
            '->ERRORR<- ERRO %s' % (e))

    # UPDATE id stripe in database
    db.update_customer_id(payment[1], payment[2], stripe_customer_id, payment[5], 'stripe')

    if not created:
        try:
            cust = stripe.Customer.retrieve(id=stripe_customer_id)
            cust = update_stripe_customer_source(cust, token)
        except Exception as e:
            error_code = e
            logger.error('->STRIPEERROR<- error %s ' % e)
    return cust, created


def p_fwd__stripe_payment(payment, stripe_token, amount_in_cents, customer, customer_type, plan_name, email=None ):
    """ Performs the payment process with stripe:
        - create a stripe.Customer related to the user if needed
        - set his card to the current card (raise if fails)
        - charge the first charge
        - set subscriptions with a trial period exactly equal to the first
        period
    The last 2 points go together to make it possible for the user to get 1
    invoice related to the first payment (sum of one-time charges and of
    the first payemnt of subscriptions).
    NB: The further subscriptions payments are handled directly by
    stripe, and their corresponding invoices are generated through the
    webhook.
    :param stripe_token: stripe.js token
    :param amount_in_cents: int amount in cents to be charged for the
    as-payment-happens-charge, including the first amount for subscriptions
    :param user_request:
    :return: is there a payment error?
    """
    payment_error = False  # Send an error tracking event in MP?
    try:
        # Create customer (commit to save the created customer id if so)
        cust, created = generate_stripe_customer_id(payment, stripe_token, email)
        logger.info(
            '->AMOUNTTOPAY<- amount to pay %s with order id %s with currency %s' % (
                amount_in_cents, payment[0],
                'eur'))
        amount_to_pay = int(amount_in_cents*100)
        try:
            charge = charge_stripe_customer_id(
                customer_id=cust.id,
                currency=payment[7],
                amount_in_cents=amount_to_pay,
                description='Payement to foqus %s_%s' % (customer, customer_type),
                order_id=payment[0]
            )
            date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            db.update_transction_id(customer, customer_type, charge.id, plan_name, date, 'stripe')
            subscribe_stripe_customer(cust.id, plan_name)
        except Exception as e:
            logger.error('->ERROR<- %s' % e)

    except Exception as e:
        logger.error('->ERRORRRR<-%s' %e)
        payment_error = True
    return payment_error
