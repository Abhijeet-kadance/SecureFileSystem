from django import forms
from .validate import validate_registerform,validate_login_form

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