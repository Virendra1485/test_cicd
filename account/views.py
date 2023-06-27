from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import SignupForm
from django.urls import reverse_lazy, reverse
from django.contrib.gis.geos import Point
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, TemplateView


class UserSignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('signin')
    template_name = 'user/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        longitude = form.cleaned_data.pop('longitude')
        latitude = form.cleaned_data.pop('latitude')
        if latitude and longitude:
            user.location = Point(float(longitude), float(latitude))
        user.save()
        return redirect(self.success_url)