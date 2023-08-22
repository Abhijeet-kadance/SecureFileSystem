from django import forms
from django.core.exceptions import ValidationError
import re
from datetime import *
from django.contrib.auth.hashers import check_password



def validate_registerform(self):
    print("Calling Validate Register Form class .....")
    register_user_name = self.cleaned_data.get('email')
    register_original_password = self.cleaned_data.get('original_password')
    register_confirm_password = self.cleaned_data.get('confirm_password')
    register_captcha_hidden = self.cleaned_data.get('captcha_hidden')
    register_captcha_input = self.cleaned_data.get('captcha_input')

    ## email reg with NON-ASCII characters
    email_regex = re.compile(r'^[\w]+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

    password_regex = re.compile(
        r'(?=.*[a-z])(?=.*[0-9])(?=.*[A-Z])(?=.*[@#$%^&+!=])[a-zA-Z0-9@#$%^&+!=]{8,20}') 
    
    if register_user_name == None or len(register_user_name) > 60:
        print("VALIDATE.PY FILE : REGISTER FORM USERNAME VALIDATION FAILED ERROR RAISED")
        raise forms.ValidationError("Enter Valid Email")
    if register_original_password == None or not re.fullmatch(password_regex, register_original_password):
        print("VALIDATE.PY FILE : REGISTER FORM PASSWORD VALIDATION FAILED ERROR RAISED")
        raise forms.ValidationError("Enter Valid Password")
    if register_confirm_password == None or not re.fullmatch(password_regex, register_original_password):
        print("VALIDATE.PY FILE : REGISTER FORM CONFIRM PASSWORD VALIDATION FAILED ERROR RAISED")
        raise forms.ValidationError("Enter valid confirm password")
    if register_captcha_input is None:
        print("VALIDATE.PY FILE : REGISTER FORM captcha_input VALIDATION FAILED ERROR RAISED ")
        raise forms.ValidationError("Please Enter Captcha")
    if len(register_captcha_input) > 5:
        print("VALIDATE.PY FILE : REGISTER FORM captcha_input VALIDATION FAILED ERROR RAISED ")
        raise forms.ValidationError("Captcha value must be of 5 charatcters only")
    if not check_password(register_captcha_input,register_captcha_hidden):
        print("VALIDATE.PY FILE : REGISTER FORM captcha_hidden VALIDATION FAILED ERROR RAISED ")
        raise forms.ValidationError("Invalid Captcha")
    

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


def validate_change_password_user_form(self):
    print("VALIDATE.PY FILE: in change_password_creation_form function")
    old_password = self.cleaned_data.get('old_password')
    new_password = self.cleaned_data.get('new_password')
    confirm_password = self.cleaned_data.get('confirm_password')

    print("VALIDATE.PY FILE : CHANGE PASSWORD FORM old_password --- ", old_password)
    print("VALIDATE.PY FILE : CHANGE PASSWORD FORM new_password --- ", new_password)
    print("VALIDATE.PY FILE : CHANGE PASSWORD FORM confirm_password --- ", confirm_password)

    print("Validate.py File : Change User Password Change validations passed : Returning clean data ---")
    return self.cleaned_data


def validate_forgot_password_form(self):
    print("VALIDATE.PY FILE: in validate_forgot_password_form function")
    email = self.cleaned_data.get('email')
    captcha_hidden = self.cleaned_data.get('captcha_hidden')
    captcha_input = self.cleaned_data.get('captcha_input')

    print("VALIDATE.PY FILE : FORGOT PASSWORD FORM EMAIL --- ", email)
    print("VALIDATE.PY FILE : FORGOT PASSWORD FORM EMAIL --- ", captcha_hidden)
    print("VALIDATE.PY FILE : FORGOT PASSWORD FORM EMAIL --- ", captcha_input)

    print("Validate.py File : Change User Forgot Password validations passed : Returning clean data ---")
    return self.cleaned_data




