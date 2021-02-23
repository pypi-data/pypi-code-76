from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class ShowSuccess(TemplateView):
    template_name = 'd_mixins/response_success.html'


class ShowInvalid(TemplateView):
    template_name = 'd_mixins/link_invalid.html'


class ShowExpired(TemplateView):
    template_name = 'd_mixins/response_expired.html'


class ShowSubmitted(TemplateView):
    template_name = 'd_mixins/response_submitted.html'


class ShowAuthorizedError(TemplateView):
    template_name = 'd_mixins/unauthorized_user.html'


class ShowSuccessPublic(TemplateView):
    template_name = 'd_mixins/public_response_success.html'


class ShowInvalidPublic(TemplateView):
    template_name = 'd_mixins/public_link_invalid.html'


class ShowExpiredPublic(TemplateView):
    template_name = 'd_mixins/public_link_expired.html'


class ShowSubmittedPublic(TemplateView):
    template_name = 'd_mixins/public_response_submitted.html'
