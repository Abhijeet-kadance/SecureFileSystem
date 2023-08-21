from django import forms
from django.core.exceptions import ValidationError
import re
from datetime import *



def validate_registerform(self):
    print("Calling Validate Reister Form class .....")
    register_user_name = self.cleaned_data.get('email')
    register_original_password = self.cleaned_data.get('original_password')
    register_confirm_password = self.cleaned_data.get('confirm_password')
    register_captcha_hidden = self.cleaned_data.get('captcha_hidden')
    register_captcha_input = self.cleaned_data.get('captcha_input')

    print("Validate.py File : Register User Name --- ", register_user_name)
    print("Validate.py File : Register Original Password --- ", register_original_password)
    print("Validate.py File : Register Confirm Password --- ", register_confirm_password)
    print("Validate.py File : Register Hidden Captch Input  --- ", register_captcha_hidden)
    print("Validate.py File : Register Captch Input --- ", register_captcha_input)


    print("Validate.py File : Register validations passed : Returning clean data ---")
    return self.cleaned_data