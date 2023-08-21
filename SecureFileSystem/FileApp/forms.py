from django import forms
from .validate import validate_registerform,validate_login_form,validate_change_password_user_form,validate_forgot_password_form

class RegisterForm(forms.Form):
    email = forms.CharField(max_length=320,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address','autocomplete':'off'}))
    original_password = forms.CharField(required=True,strip=False,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password','name':'original_password'}))
    confirm_password = forms.CharField(required=True,strip=False,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password Again','name':'confirm_password'}))
    captcha_hidden = forms.CharField(widget=forms.HiddenInput(),required="False")
    captcha_input = forms.CharField(max_length=5,required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Captcha','name':'captcha'}))


    def clean(self):
        super(RegisterForm,self).clean()
        validate_registerform(self)

class LoginForm(forms.Form):
    username = forms.EmailField(max_length=320, required=True,widget=forms.TextInput(attrs={'class':'form-control','id':'inputEmail','placeholder':"Enter Email",'autocomplete':'off'}))
    password = forms.CharField(required=True,strip=True,widget=forms.PasswordInput(attrs={'class':'form-control','id':'inputPassword','placeholder':'Enter Password','name':'password'}))

    captcha_hidden = forms.CharField(widget=forms.HiddenInput(), required="False")
    captcha_input = forms.CharField(max_length=5, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'inputCaptcha', 'placeholder': 'Enter Captcha', 'name': 'captcha'}))
    
    def clean(self):
        print("FORMS.PY FILE : CLEAN METHOD CALLING")
        # data is feteched using the super function of django
        super(LoginForm, self).clean()
        validate_login_form(self)

class ChangePasswordUserForm(forms.Form):
    old_password = forms.CharField(min_length=8,max_length=20,required=True,strip=False,widget=forms.PasswordInput(attrs={'class':'form-control','id':'inputOldPassword','placeholder':"Enter Old Password",'name':'old_password'}))
    new_password = forms.CharField(min_length=8,max_length=20,required=True,strip=False,widget=forms.PasswordInput(attrs={'class':'form-control','id':'inputNewPassword','placeholder':"Enter New Password",'name':'new_password'}))
    confirm_password = forms.CharField(min_length=8,max_length=20,required=True,strip=False,widget=forms.PasswordInput(attrs={'class':'form-control','id':'inputConfirmPassword','placeholder':"Enter Confirm Password",'name':'confirm_password'}))

    def clean(self):
        print("FORMS.PY FILE : CLEAN METHOD CALLING")
        super(ChangePasswordUserForm, self).clean()
        validate_change_password_user_form(self)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=60, required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id': 'inputEmail', 'placeholder': 'Enter Email', 'autocomplete': 'off'}))
    
    captcha_hidden = forms.CharField(widget=forms.HiddenInput(), required="False")
    captcha_input = forms.CharField(max_length=5, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'inputCaptcha', 'placeholder': 'Enter Captcha', 'name': 'captcha'}))
    
    def clean(self):
        print("FORMS.PY FILE : CLEAN METHOD CALLING")
        # data is feteched using the super function of django
        super().clean()
        validate_forgot_password_form(self)
