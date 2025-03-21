from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from .models import Video

class HomePageView(ListView):
    template_name = "homepage.html"
    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["videos"] = Video.objects.filter().order_by("-pub_date")[:50]
        return context
