"""Real signature module."""
from django.core import signing
from django.core.exceptions import ValidationError
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse,
    HttpResponse,
)
from django.middleware import csrf
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_safe
from sentry_sdk import capture_message, capture_exception

from appel_crises.captcha import verify_captcha
from appel_crises.challenges import check_answer_from_signed_challenge_id
from appel_crises.data import (
    POSTAL_CODE_TO_DISTRICT,
    DISTRICT_TO_MP,
    CAPTCHA_FAILURE_REASONS_TRANSLATIONS,
)
from appel_crises.models import Signature, CallOutEmail, BlackListedEmail
from appel_crises.views import error_no_js


@require_POST
def sign(request: HttpRequest):
    """Main signature function"""
    # noinspection PyArgumentList
    try:
        first_name = request.POST['firstname']
        surname = request.POST['surname']
        email = request.POST['email']
        answer = request.POST['challenge_answer']
        signed_challenge_id = request.POST['challenge_id']
        news = request.POST.get('news', 'off')
    except KeyError as e:
        return error_no_js(
            request,
            title=f"Le champs {e} est requis.",
            text="Veuillez remplir complètement le formulaire.",
        )

    if news == 'on':
        news = True
    else:
        news = False

    # challenge
    try:
        is_valid = check_answer_from_signed_challenge_id(signed_challenge_id, answer)
        if not is_valid:
            raise ValueError(
                f"Invalid answer on challenge '{signed_challenge_id}': '{answer}'"
            )
    except (signing.BadSignature, ValueError) as e:
        capture_exception(e)
        return error_no_js(
            request,
            title="Erreur lors de la vérification du challenge",
            text="Votre réponse ne correspondait pas. Veuillez ré-essayer.",
        )

    if BlackListedEmail.is_blacklisted(email):
        capture_message("Blacklisted email: " + email)
        return HttpResponseBadRequest()

    signature = Signature(
        first_name=first_name,
        surname=surname,
        email=email,
        has_captcha_verified=False,
        news=news,
    )

    try:
        # Validate, among other things, the uniqueness of the email
        signature.full_clean()
    except ValidationError as e:
        # Probably a duplicate email, or a wrong email, or too long values
        capture_exception(e)
        return error_no_js(
            request,
            title="Nous n'avons pas pu prendre en compte votre signature.",
            text="Votre email a sûrement déjà été utilisé: <br/>"
            + "<br/>".join(e.messages),
        )

    # I would put a try catch, but at this point i don't know what could go wrong
    signature.save()

    return redirect('success')


def captcha_failure_message(failure_reasons):
    return "Erreur vérification captcha : {}".format(
        ", ".join(
            CAPTCHA_FAILURE_REASONS_TRANSLATIONS.get(reason, reason)
            for reason in failure_reasons
        )
    )


@require_POST
@csrf_exempt
def sign_ajax(request: HttpRequest):
    """Main signature function"""
    # noinspection PyArgumentList
    try:
        first_name = request.POST['firstname']
        surname = request.POST['surname']
        email = request.POST['email']
        captcha_token = request.POST['mtcaptcha-verifiedtoken']
        news = 'news' in request.POST and request.POST['news'] == 'on'
    except KeyError as e:
        capture_message(f"Sign-ajax failed, missing key {e}")
        return HttpResponseBadRequest(f"Le champs {e} est requis.")

    captcha_valid, failure_reasons = verify_captcha(captcha_token)
    if not captcha_valid:
        message = "Erreur vérification captcha : " + ", ".join(failure_reasons)
        capture_message(message)
        return HttpResponseBadRequest(message)

    if BlackListedEmail.is_blacklisted(email):
        capture_message("Blacklisted email: " + email)
        return HttpResponseBadRequest()

    signature = Signature(
        first_name=first_name,
        surname=surname,
        email=email,
        news=news,
        has_captcha_verified=True,
    )

    try:
        # Validate, among other things, the uniqueness of the email
        signature.full_clean()
    except ValidationError as e:
        capture_exception(e)
        # Probably a duplicate email, or a wrong email, or too long values
        return HttpResponseBadRequest("<br/>".join(e.messages))

    # I would put a try catch, but at this point i don't know what could go wrong
    signature.save()
    return HttpResponse(status=200)


@require_POST
@csrf_exempt
def call_out_ajax(request: HttpRequest):
    """Form submission via an XHR request in the browser"""
    try:
        captcha_token = request.POST['mtcaptcha-verifiedtoken']
    except KeyError as e:
        capture_message(f"Call-Out-ajax failed, missing key {e}")
        return HttpResponseBadRequest(f"Missing field {e}")

    captcha_is_valid, captcha_failures = verify_captcha(captcha_token)
    if not captcha_is_valid:
        message = "Invalid captcha token : " + ", ".join(captcha_failures)
        capture_message(message)
        return HttpResponseBadRequest(message)

    fields = [
        "content",
        "subject",
        "send_to_government",
        "circonscription_numbers",
        "sender",
        "from_email",
        "postal_code",
        "template_id",
    ]
    try:
        values = {field: request.POST[field] for field in fields}
    except KeyError as e:
        capture_message(f"Call-Out-ajax failed, missing key {e}")
        return HttpResponseBadRequest(e)

    call_out_email = CallOutEmail(**values)
    call_out_email.send_to_government = int(call_out_email.send_to_government)

    if BlackListedEmail.is_blacklisted(call_out_email.from_email):
        capture_message("Blacklisted email: " + call_out_email.from_email)
        return HttpResponseBadRequest()

    try:
        call_out_email.template_id = int(call_out_email.template_id)
    except ValueError:
        call_out_email.template_id = None

    try:
        call_out_email.full_clean()
    except ValidationError as e:
        # Probably a duplicate email, or a wrong email, or too long values
        capture_exception(e)
        return HttpResponseBadRequest(e)

    if any(
        number not in DISTRICT_TO_MP
        for number in call_out_email.circonscription_numbers.split(',')
        if len(number) > 0
    ):
        message = (
            "Circonscription number not found: '"
            + call_out_email.circonscription_numbers
            + "'"
        )
        capture_message(message)
        return HttpResponseBadRequest(message)

    call_out_email.save()

    return HttpResponse(status=200)


@require_POST
def call_out(request: HttpRequest):
    """Form submission from no js page"""
    fields = [
        "content",
        "subject",
        "sender",
        "from_email",
        "postal_code",
        "template_id",
    ]
    try:
        values = {field: request.POST[field] for field in fields}
    except KeyError as e:
        capture_exception(e)
        return error_no_js(
            request,
            title="Valeur manquante: " + str(e),
            text="Veuillez remplir le formulaire complètement.",
        )

    call_out_email = CallOutEmail(**values)

    if BlackListedEmail.is_blacklisted(call_out_email.from_email):
        capture_message("Blacklisted email: " + call_out_email.from_email)
        return HttpResponseBadRequest()

    # noinspection PyCallByClass,PyTypeChecker
    if request.POST.get("send_to_government", "off") == 'on':
        call_out_email.send_to_government = 1
    else:
        call_out_email.send_to_government = False

    try:
        call_out_email.full_clean()
    except ValidationError as e:
        # Probably a duplicate email, or a wrong email, or too long values
        capture_exception(e)
        return error_no_js(
            request,
            title="Votre formulaire n'a pas pu être validé.",
            text="Votre adresse email a sûrement déjà été soumise:"
            + "<br />".join(e.messages),
        )

    # noinspection PyTypeChecker,PyCallByClass
    if request.POST.get("send_to_depute", False):
        postal_code = call_out_email.postal_code
        if postal_code not in POSTAL_CODE_TO_DISTRICT:
            capture_message(f"Code postal not found: '{postal_code}'")
            return error_no_js(
                request,
                status=404,
                title="Nous n'avons pas trouvé votre code postal.",
                text="Veuillez rentrer un code à 5 chiffres. Si vous pensez que "
                "notre base de données est incomplète, vous pouvez essayer le "
                "code postal de la ville principale de votre circonscription.",
            )

        circo_number = POSTAL_CODE_TO_DISTRICT[postal_code][0]
        if circo_number not in DISTRICT_TO_MP:
            capture_message(f"Circonscription not found: '{circo_number}'")
            return error_no_js(
                request,
                status=404,
                title="Nous n'avons pas trouvé votre circonscription.",
                text="Veuillez réessayer, ou envoyer un mail "
                "directement à votre député.",
            )

        call_out_email.circonscription_numbers = circo_number

    call_out_email.save()

    return redirect("success-email")


@require_safe
@cache_control(max_age=60)
def search_depute(request: HttpRequest):
    """Take input as POST parameter and return the corresponding depute as JSON"""

    # noinspection PyCallByClass,PyTypeChecker
    postal_code = request.GET.get('postal_code', '')

    if postal_code not in POSTAL_CODE_TO_DISTRICT:
        capture_message(f"Postal code not found '{postal_code}'")
        return HttpResponseNotFound()

    districts = POSTAL_CODE_TO_DISTRICT[postal_code]

    mp_data = [(*DISTRICT_TO_MP[d], d) for d in districts if d in DISTRICT_TO_MP]

    # We have to pass safe=False, because we want to serialize an Array, see:
    # https://docs.djangoproject.com/en/3.0/ref/request-response/#serializing-non-dictionary-objects
    return JsonResponse(mp_data, safe=False)


@require_safe
@never_cache
def get_csrf_token(request: HttpRequest):
    """
    Return a CSRF token. Nothing big to do here, everything is done by the CSRF
    middleware.
    """
    # Force setting the token cookie on the response.
    csrf.get_token(request)
    return HttpResponse('')


@require_safe
@never_cache
def version(request):
    from appel_crises import __version__

    return HttpResponse(__version__)
