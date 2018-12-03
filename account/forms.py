from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password' , widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name','username','email',)
        help_texts = {'username': None,'email': None,}   #To heddin help_text
# Hidden Help text for password
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
# Hidden help Text for all
    # def __init__(self, *args, **kwargs):
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)
    #
    #     for fieldname in ['username', 'password', 'password2']:
    #         self.fields[fieldname].help_text = None

# another way to Hidden help_text
    # class Meta:
    #         model = User
    #         fields = ("username", "email", "password1", "password2")
    #         help_texts = {
    #             'username': None,
    #             'email': None,
    #         }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name' , 'last_name' , 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
