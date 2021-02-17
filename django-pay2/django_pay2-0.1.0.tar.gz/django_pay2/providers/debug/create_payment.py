from django_pay2.decorators import handle_debug


@handle_debug
def create_debug_payment(request, amount, desc, receiver):
    raise NotImplementedError
