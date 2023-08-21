from django import forms
from django.core.exceptions import ValidationError
import re
from datetime import *



def validate_registerform(self):
    print("Calling Validate Register Form class .....")
    register_user_name = self.cleaned_data.get('email')
    register_original_password = self.cleaned_data.get('original_password')
    register_confirm_password = self.cleaned_data.get('confirm_password')
    register_captcha_hidden = self.cleaned_data.get('captcha_hidden')
    register_captcha_input = self.cleaned_data.get('captcha_input')

    print("Validate.py File : Register User Name --- ", register_user_name)
    # print("Validate.py File : Register Original Password --- ", register_original_password)
    # print("Validate.py File : Register Confirm Password --- ", register_confirm_password)
    # print("Validate.py File : Register Hidden Captch Input  --- ", register_captcha_hidden)
    # print("Validate.py File : Register Captch Input --- ", register_captcha_input)


    print("Validate.py File : Register validations passed : Returning clean data ---")
    return self.cleaned_data


def validate_login_form(self):
    print("Calling Validate Login Form class .....")
    login_username = self.cleaned_data.get('username')
    login_password = self.cleaned_data.get('password')
    login_captcha_hidden = self.cleaned_data.get('captcha_hidden')
    login_captcha_input = self.cleaned_data.get('captcha_input')

    print("Validate.py File : Login User Name --- ", login_username)
    # print("Validate.py File : Login password --- ", login_password)

    print("Validate.py File : Login validations passed : Returning clean data ---")
    return self.cleaned_data



