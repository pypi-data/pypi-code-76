from django.views.generic import TemplateView

from .forms import TestForm


class TestView(TemplateView):
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TestForm()
        return context
