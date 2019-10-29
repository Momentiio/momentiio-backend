from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import File, PrivateFile


class FileCreateView(CreateView):
    model = File
    fields = ['upload', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        files = File.objects.all()
        context['file'] = files
        return context
