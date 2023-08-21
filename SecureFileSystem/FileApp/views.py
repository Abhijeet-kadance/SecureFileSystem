from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .custom_captcha import captcha_img_generator, random_captcha_generator
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.conf import settings
from datetime import datetime, timedelta,timezone

# Create your views here.
def index(request):
    return render(request, 'FileApp/index.html')


def regiter_view(request):

    # Inside Register View
    print('--- Calling Register View---')
    
    # Checking if any POST request has been made
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('original_password')

            print('User email : ' , email)
            print('User password : ' , password)

            # Check to see if the user details does not exists
            # print('User name : ', User.objects.get(username=email))
            if not User.objects.filter(username=email).exists():
                print('User does not exist')
                user = User.objects.create(email=email, username=email)
                user.set_password(password)
                user.save()
            else:
                user = User.objects.get(username=email)
                print('Duplicate User : ', user)

                if not user.is_active:
                    user.set_password(password)
                    user.save()
                else:
                    print("User Already Exists....")
                    return render(request,"FileApp/Registeration_Form.html",{'form':form})
                
            if not user == None:
                domain = request.get_host()
                # urlsafe_base64_encode is used to Encode a bytestring to a base64 string for use in URLs. Strip any trailing equal signs.
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # make_toke is used to create a token that can be used once to do a password reset for the given user.
                token = account_activation_token.make_token(user)
                # 
                link = reverse('user_activate',kwargs={"uid64":uid,"token":token})
                activate_link = "http://" + domain + link
                print("Activate Link :" , activate_link)


                try:
                    send_mail(subject="Registration Successful",message='',from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=[email],fail_silently=False,html_message="Your registration is successful. To activate your accout please click on activation link:  "+'</br><a href={0}>{0}</a>'.format(activate_link))
                    print("Email Sent SuccessFully !!!")

                except:
                    print("Email Not Sent !!!")
        else:
            print("Unsuccessful registration. Invalid information.")
        

        return render(request,"FileApp/Registeration_Form.html", context={"form": form})
    
    else:
        form = RegisterForm()
        captcha_value = random_captcha_generator()
        captcha_img_generator(captcha_value)
        form.fields['captcha_hidden'].initial = make_password(captcha_value)

        
    return render(request,"FileApp/Registeration_Form.html", context={"form": form})
   

def user_activate_view(request,uid64,token):
    # For reference of force_str and force_bytes check the documentation link below
    # https://docs.djangoproject.com/en/4.0/ref/utils/#module-django.utils.encoding

    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    joined_date = user.date_joined
    expiry_date = joined_date + timedelta(hours=24)

    print("Expiry Date : " , expiry_date)

    if (expiry_date > datetime.now(timezone.utc)):
        if user is not None and account_activation_token.check_token(user,token):
            user.isactive = True
            user.save()
            print("User activation Done ....")
        else:
            if user.is_active == True:
                print("User already Activated..")
            else:
                form = RegisterForm()
                return render(request,'FileApp/Registeration_form.html',context={"form":form})
        return redirect('login')
    else:
        return render(request,'FileApp/Registeration_form.html')
    
def login_view(request):
    return render(request,'FileApp/Login.html')

