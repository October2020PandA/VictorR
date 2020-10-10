from django import forms
# from .models import Users
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=45, required=True)
    last_name = forms.CharField(max_length=45, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if len(cleaned_data['first_name']) < 2:
            self.add_error('first_name', "First name must be at least 2 characters")
        if len(cleaned_data['last_name']) < 2:
            self.add_error('last_name', "Last name must be at least 2 characters")
        existing_user = authenticate(email=cleaned_data['email'], password=cleaned_data['password1'])

class LogForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


# IF NOT USING AUTH FEATURE
# class UserForm(forms.ModelForm):
#     password = forms.CharField(max_length=100, widget=forms.PasswordInput)
#     confirm_pw = forms.CharField(max_length=100, widget=forms.PasswordInput)
#     class Meta:
#         model = Users
#         fields = '__all__'

#     def clean(self):
#         cleaned_data = super(UserForm, self).clean()
#         if len(cleaned_data['first_name']) < 2:
#             self.add_error('first_name', "First name must be at least 2 characters")
#         if len(cleaned_data['last_name']) < 2:
#             self.add_error('last_name', "Last name must be at least 2 characters")
#         existing_user = Users.objects.filter(email=cleaned_data['email'])
#         if len(existing_user) > 0:
#             self.add_error('email', "Email already exist")
#         if cleaned_data['password'] != cleaned_data['confirm_pw']:
#             self.add_error('password', "Password does not match")