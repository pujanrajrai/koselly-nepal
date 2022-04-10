from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from .models import Profile
from datetime import date
from .forms import ProfileForms, ProfileUpdateForms


class CreateProfile(CreateView):
    form_class = ProfileForms
    template_name = 'myprofile/profile_create_update.html'

    def get_success_url(self):
        return reverse_lazy('my_profile:profile_list_view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user
        return kwargs

    def get(self, *args, **kwargs):
        if Profile.objects.filter(user__email=self.request.user).exists():
            return redirect('my_profile:profile_list_view')
        return super(CreateProfile, self).get(*args, **kwargs)


class ProfileListView(ListView):
    model = Profile
    template_name = 'myprofile/profile_view.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = Profile.objects.filter(user__email=self.request.user)
        return queryset

    def get(self, *args, **kwargs):
        if not Profile.objects.filter(user__email=self.request.user).exists():
            return redirect('my_profile:profile_create')
        return super(ProfileListView, self).get(*args, **kwargs)


class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdateForms
    success_url = "/profile/view/"
    template_name = 'myprofile/update_profile.html'
    model = Profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user
        return kwargs

