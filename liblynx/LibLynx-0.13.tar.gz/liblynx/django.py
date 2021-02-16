import logging
import liblynx
from django.conf import settings
from django.http import HttpResponseRedirect


class LibLynxAuthMiddleware:
    def __init__(self, get_response):
        self.ll = liblynx.Connect()
        logging.debug(
            f"LibLynx API connected with access_token: {self.ll.access_token}"
        )
        self.get_response = get_response
        self.product_cache = {}

    def authenticate(self, request):
        host = request.META.get("HTTP_X_FORWARDED_FOR", "127.0.0.127")
        abs_uri = request.build_absolute_uri()
        user_agent = request.headers.get("User-Agent", "<unknown>")

        logging.debug(
            f"Trying New identification for \nhost: [{host}]\nurl: [{abs_uri}]\nuser agent: [{user_agent}]",
        )
        identification = self.ll.new_identification(host, abs_uri, user_agent)
        logging.debug(identification)

        if (
            "_ll_allow_wayf" in request.GET and identification["status"] == "wayf"
        ):  # Needs a redirect to authenticate
            return HttpResponseRedirect(identification["_links"]["wayf"]["href"])

        if identification["status"] == "identified":
            request.session["LIBLYNX_ACCOUNT"] = identification["account"][
                "account_name"
            ]
            request.session["LIBLYNX_ACCOUNT_ID"] = identification["account"].get("publisher_reference", "?")

            # Get the account information, so that we can retrieve the subscriptions
            account = self.ll.api(
                "account", identification["account"]["_links"]["self"]["href"],
            )
            logging.debug(account)

            # Fetch the products for this user, if configured
            if settings.LIBLYNX_FETCH_PRODUCTS:
                subs = self.ll.api("subs", account["_links"]["account_subs"]["href"])

                products = []
                for sub in subs["subscriptions"]:
                    sub_link = sub["_links"]["subscription_units"]["href"]
                    if sub_link not in self.product_cache:
                        self.product_cache[sub_link] = self.ll.api("sub", sub_link)
                    for unit in self.product_cache[sub_link]["units"]:
                        products.append(unit["unit_code"])

                request.session["LIBLYNX_PRODUCTS"] = products
                logging.debug(f"Products found {products}")
        elif identification["status"] == "wayf":
            # Not idenitified if we get to there, so make it anonymous
            request.session["LIBLYNX_ACCOUNT"] = ""
            request.session["LIBLYNX_ACCOUNT_ID"] = "anon"

    def __call__(self, request):
        if "LIBLYNX_ACCOUNT" not in request.session or "_ll_allow_wayf" in request.GET:
            response = self.authenticate(request)
            if response is not None:
                return response

        response = self.get_response(request)

        return response
