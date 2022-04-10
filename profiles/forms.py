from django import forms

from accounts.models import MyUser
from .models import Profile


class ProfileForms(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'photo', 'full_name', 'phone_number', 'dob', 'gender', 'default_shipping_address']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'default_shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user_id, *args, **kwargs):
        super(ProfileForms, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Select Gender'
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = MyUser.objects.filter(email=user_id)


class ProfileUpdateForms(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'photo', 'full_name', 'phone_number', 'dob', 'gender', 'default_shipping_address']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'default_shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user_id, *args, **kwargs):
        super(ProfileUpdateForms, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Select Gender'
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = MyUser.objects.filter(email=user_id)
