from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Submit, Row


CERT_STATUS = (
    ('Collected', 'Collected'),
    ('Not collected', 'Not collected')
)

FEE_STATUS = (
    ('Ongoing', 'Ongoing'),
    ('Completed', 'Completed')
)
class FeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fee_required', 'fee_paid', 'fee_status']

class CertUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['cert_status']

class ExamUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['results']
        
# class StudentSearchForm(forms.ModelForm):
#     full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
#        'class': 'form-control',
#      }))
#     reg_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
#        'class': 'form-control',
#      }))
#     class Meta:
#         model = Student
#         fields = ['full_name', 'reg_number']

class StudentAccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['fee_required', 'fee_paid', 'fee_balance', 'user', 'fee_status', 'cert_status', 'results' ]
    
    

# The pwdChangeForm is a subclass of 'PassswordChangeForm' and inherits from it       
class pwdChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder': 'Old password..', 'id': 'form-oldpass'}
    ))
    new_password1 = forms.CharField(label='New Password1', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder': 'New password..', 'id': 'form-newpass1'}
    ))
    new_password2 = forms.CharField(label='New Password2', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder': 'Confirm password..', 'id': 'form-newpass2'}
    ))
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_username(self):
    #         username = self.cleaned_data['username']
    #         if User.objects.filter(username=username).exists():
    #             raise forms.ValidationError('name is not available')
    #         return username

    # def clean_email(self):
    #         email = self.cleaned_data['email']
    #         if User.objects.filter(email=email).exists():
    #             raise forms.ValidationError('email is not available')
    #         return email
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update(
    #         {'class': 'form-control mb-3', 'placeholder': 'Username'})
    #     self.fields['email'].widget.attrs.update(
    #         {'class': 'form-control mb-3', 'placeholder': 'E-mail'})
    #     self.fields['password1'].widget.attrs.update(
    #         {'class': 'form-control', 'placeholder': 'Password'})
    #     self.fields['password2'].widget.attrs.update(
    #         {'class': 'form-control', 'placeholder': 'Repeat Password'})

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
       'class': 'form-control',
       'placeholder': 'First name',
     }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name',
     }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
     }))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your message',
     }))
    class Meta:
        model= Contact
        fields = '__all__'




#class StudentCreationForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = '__all__'
#         exclude = ['user', 'fee_balance']

#     def __init__(self, *args, **kwrgs):
#             super().__init__(*args, **kwrgs)
#             self.helper = FormHelper()
#             self.helper.form_method = 'post'
#             self.helper.add_input(Submit('save', 'Save'))

#             self.helper.layout = Layout(
#                 Row(
#                     Column('full_name'),
#                     Column('reg_number'),
#                 ),
#                 Row(
#                     Column('phone'),
#                     Column('email'),
#                 ),
#                 Row(
#                     Column('course_name'),
#                     Column('course_level'),
#                 ),
#                 Row(
#                     Column('fee_required'),
#                     Column('fee_paid'),
#                 ),
#                 Row(
#                     Column('fee_status'),
#                     Column('cert_status'),
#                 ),
#             )
# class StudentUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = '__all__'
#        exclude = ['fee_required', 'fee_paid', 'fee_balance', 'user']