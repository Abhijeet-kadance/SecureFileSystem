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
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
 
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
                user.is_active = False
                user.save()
            else:
                user = User.objects.get(username=email)
                print('Duplicate User : ', user)

                if not user.is_active:
                    user.set_password(password)
                    user.save()
                else:
                    print("User Already Exists....")
                    messages.error(request, "User Already Exists", extra_tags='danger') 
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
                    messages.success(request, 'User Registered Successfully. Please Check mail for Activation Link !!!', extra_tags='success')
                    return redirect('register_view')
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
            user.is_active = True
            user.save()
            print("User activation Done ....")
            messages.success(request, "User has been activated.", extra_tags='danger') 
        else:
            if user.is_active == True:
                print("User already Activated..")
                messages.success(request, 'User Already Activated', extra_tags='success')
            else:
                form = RegisterForm()
                return render(request,'FileApp/Registeration_form.html',context={"form":form})
        return redirect('login')
    else:
        return render(request,'FileApp/Registeration_form.html')
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print("username : " + username + " password : " + password)

            try:
                if User.objects.filter(username=username,is_active=False):
                    print("User is not acive...")
                    messages.error(request, "User is not Active", extra_tags='danger') 
                else:
                    user = authenticate(username=username,password=password)
                    print(user)
                    if user is not None:
                        login(request,user)
                        return redirect('dashboard')
                    else:
                        print("User Credentials Incorrect ....")
                        messages.error(request, "Incorrect User Credentials", extra_tags='danger') 
            except:
                print("Something went Wrong Try login Again")
                messages.error(request, "Something went Wrong Try login Again", extra_tags='danger') 
        else:
            print("Form is invalid")
            captcha_value = random_captcha_generator()
            captcha_img_generator(captcha_value)
            form.data['captcha_input'] = ''
            form.data['captcha_hidden'] = make_password(captcha_value)
    else:
        form = LoginForm()
        captcha_value = random_captcha_generator()
        captcha_img_generator(captcha_value)
        print("captcha value ", captcha_value)
        form.fields['captcha_hidden'].initial = make_password(captcha_value)

    return render(request,'FileApp/Login.html',{'form':form})

@login_required()
def logout_view(request):
    
    logout(request)
    
    # messages.success(request, "You are successfully logged Out", extra_tags="success")
    return redirect("login")

def dashboard_view(request):
    return render(request,'FileApp/Dashboard.html')


def captcha_refresh(request):
    print("In captcha refresh method")

    captcha_value = random_captcha_generator()
    captcha_img_generator(captcha_value)
    print("captcha Value ", captcha_value)

    return JsonResponse({'captcha_value': f'{make_password(captcha_value)}', 'captcha_url': '/captcha_images/CAPTCHA.png'})


def change_password_view(request):
    print("in change password view")
    form = ChangePasswordUserForm()
    try:
        user = User.objects.get(username=request.user)
        print("user ", user)
        if request.method == 'POST':
            form = ChangePasswordUserForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                
                print("old : ", old_password , " new : ", new_password)
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Passowrd changed successfully', extra_tags='success')
                else:
                    messages.error(request, "Incorrect Old Password", extra_tags='danger')                
            else:
                print("invalid form")
    except:
        messages.error(request, "User Not Found", extra_tags='danger')

    return render(request, 'FileApp/ChangePassword.html', {'form':form})


def forgot_password_view(request):
    form = ForgotPasswordForm()
    return render(request, 'FileApp/ForgetPassword.html',{'form':form})




@login_required()
def download_new(request):

    download_obj = Material.objects.all()
    download_approval_obj = MaterialApproval.objects.all()
    download_catergory_obj = MaterialCategory.objects.all().order_by('id')
    
    #material_filter_object = Material.objects.filter(Material_CategoryType__in=selected_category)
   


    if request.method == 'POST':
        print("Download Section Starts ................")
        if request.POST.get('download_new'):
            print("Called download Material Section ................")
            ## FETCHING MATERIAL ID 
            Materials_id = request.POST.get('download_new')
            Material_obj = Material.objects.get(pk=Materials_id)
            User_all_data = MaterialApproval.objects.filter(Requested_User_id=request.user.id)
            print("User all data : " , User_all_data.values('Material_id'))

            MaterialPerUser = User_all_data.filter(Material_id=Materials_id)
            if not MaterialPerUser :
                b = MaterialApproval(Material=Material_obj,Approval_Status="---",Requested_User=request.user)
                b.save()
                messages.success(request, 'Download request submitted for Approval !!', extra_tags='success')
                print("Downloaded Successfully")
            else:
                messages.error(request, "Document Already Requested !!", extra_tags='danger')           
                print("Download Requestes Already....")
                # messages.success(request, 'Download request submitted for Approval !!', extra_tags='success')
        
        if request.POST.get('select_category'):
            print("Inside Filter method")
            selected_category = request.POST.getlist('select_category')
            if selected_category == '':
                print("No Selected Category")
            else:
                print("selected")
            print("Selected :" ,selected_category)
           
            request.session['selected_categories'] = selected_category
            # paginator = Paginator()
            material_filter_object = Material.objects.filter(Material_CategoryType__in=selected_category)
            download_obj = material_filter_object
            
            print(material_filter_object)
            paginator = Paginator(material_filter_object,2)
            page_number = request.GET.get('page')
            Page_data = paginator.get_page(page_number)
            totalpages = Page_data.paginator.num_pages
            # updated_list = [eval(i) for i in selected_category]
            context = {
                "download_obj": Page_data,
                "download_approval_obj":download_approval_obj,
                "download_catergory_obj":download_catergory_obj,
                "selected_category":selected_category,
                "totalPageList":[n+1 for n in range(totalpages)]
            }
            return render(request, 'FileApp/Download.html',context)
        
        if request.POST.get('reset'):
            print("Inside reset method ....")
            reset_obj = Material.objects.all()

            try:
                print("Inside reset session ....")
                del request.session['selected_categories']
            except KeyError:
                pass

            context = {
                "download_obj": reset_obj,
                "download_approval_obj":download_approval_obj,
                "download_catergory_obj":download_catergory_obj,
            }
            return render(request, 'FileApp/Download.html',context)
            
    else:
        print("Please choose file to donwload")

    if 'visited' in request.session:
        print("data :",request.session.get('selected_categories', ''))
        session_data = request.session.get('selected_categories', '')
        
        print("Sessionnnnnnn :",session_data)
        if session_data:
            print("Session Data Available")
            material_filter_object = Material.objects.filter(Material_CategoryType__in=session_data)
        else:
            print("Session Data Not available")
            material_filter_object = Material.objects.all()
        
        paginator1 = Paginator(material_filter_object,2)
        page_number = request.GET.get('page')
        Page_data = paginator1.get_page(page_number)
        totalpages = Page_data.paginator.num_pages
        context = {
                # 'download_catergory_obj':download_catergory_obj,
                # 'download_obj':download_obj,
                "download_obj": Page_data,
                "download_approval_obj":download_approval_obj,
                "download_catergory_obj":download_catergory_obj,
                "totalPageList":[n+1 for n in range(totalpages)],
            }

        return render(request, 'FileApp/Download.html',context)
    else:
        request.session['visited'] = True
        print("Session does not exist")
        download_obj = Material.objects.all()
        
        paginator1 = Paginator(download_obj,2)
        page_number = request.GET.get('page')
        Page_data = paginator1.get_page(page_number)
        totalpages = Page_data.paginator.num_pages
        context = {
                # 'download_catergory_obj':download_catergory_obj,
                # 'download_obj':download_obj,
                "download_obj": download_obj,
                "download_approval_obj":download_approval_obj,
                "download_catergory_obj":download_catergory_obj,
                "totalPageList":[n+1 for n in range(totalpages)],
            }

        return render(request, 'FileApp/Download.html',context)

        





def download_view(request):
    download_obj = Material.objects.all()
    download_approval_obj = MaterialApproval.objects.all()
    download_catergory_obj = MaterialCategory.objects.all().order_by('id')

    print(download_catergory_obj)
    paginator1 = Paginator(download_obj,2)
    page_number = request.GET.get('page')
    Page_data = paginator1.get_page(page_number)
    totalpages = Page_data.paginator.num_pages

    if request.user.is_authenticated:
        print("User is authenticated ")
        if request.method == 'POST':
            
            print("Selected categories : " , request.POST.getlist('select_category'))
            if request.POST.get('download'):
                print("Download Form")
                Materials_id = request.POST.get('download')
                Material_obj = Material.objects.get(pk=Materials_id)
                if MaterialApproval.objects.filter(Q(Requested_User_id=request.user.id) & Q(Material_id=int(Materials_id))).exists():
                    print("Document Already Requeted")
                    messages.error(request, "Document Already Requested !!", extra_tags='danger')           
                else:
                    b = MaterialApproval(Material=Material_obj,Approval_Status="---",Requested_User=request.user)
                    b.save()
                    messages.success(request, 'Download request submitted for Approval !!', extra_tags='success')
            
            # Filter By Category Logic 
            elif request.POST.get('select_category'):
                print("Inside Filter method")
                selected_category = request.POST.getlist('select_category')
                
                request.session['selected_categories'] = selected_category
                # paginator = Paginator()
                material_filter_object = Material.objects.filter(Material_CategoryType__in=selected_category)
                print(material_filter_object)
                paginator = Paginator(material_filter_object,2)
                page_number = request.GET.get('page')
                Page_data = paginator.get_page(page_number)
                totalpages = Page_data.paginator.num_pages
                updated_list = [eval(i) for i in selected_category]
                context = {
                    "download_obj": Page_data,
                    "download_approval_obj":download_approval_obj,
                    "download_catergory_obj":download_catergory_obj,
                    "selected_category":selected_category,
                    "totalPageList":[n+1 for n in range(totalpages)]
                }
                return render(request, 'FileApp/Download.html',context)
            elif request.POST.get('reset'):
                print("Inside reset method ....")
                reset_obj = Material.objects.all()

                try:
                    print("Inside reset session ....")
                    del request.session['selected_categories']
                except KeyError:
                    pass

                context = {
                    "download_obj": reset_obj,
                    "download_approval_obj":download_approval_obj,
                    "download_catergory_obj":download_catergory_obj,
                }
                return render(request, 'FileApp/Download.html',context)
            
            else:
                print("Please tick the checkbox first")
                messages.error(request, "Please tick the checkbox first", extra_tags='danger')           

    else:
        print("Please Login First")
        messages.error(request,"Please Login First to download", extra_tags='danger')
    context = {
        "download_obj": Page_data,
        "download_approval_obj":download_approval_obj,
        "download_catergory_obj":download_catergory_obj,
        "totalPageList":[n+1 for n in range(totalpages)],
        # "selected_category":selected_category,
    }
    return render(request, 'FileApp/Download.html',context)

# def download_filter_view(request):
#     print("Inside DownloadFilterView...")
#     return render(request,'FileApp/Download.html')


def admin_material_approval(request):
    
    if request.method == "POST":
        print("In POST method")    
        approval_status = request.POST.get('approval_status')
        material_id = request.POST.get('material_id')
        print("Material ID : ", material_id)
        try:
            material_approval_obj = MaterialApproval.objects.get(id=material_id)
            print(material_approval_obj)
            if approval_status == 'yes':
                print("approval status : YES")
                
                MaterialApproval.objects.filter(id=material_approval_obj.id).update(Approval_Status='YES')
                
            elif approval_status == 'no':
                print("approval status : NO")
                MaterialApproval.objects.filter(id=material_approval_obj.id).update(Approval_Status='NO')
            else:
                print("approval status : None")
                messages.error(request, "Please choose valid category")
        except:
            messages.error(request, "Material does not exist")
    
    materials_for_approval = MaterialApproval.objects.filter(Approval_Status='---')
    approved_materials = MaterialApproval.objects.filter(Q(Approval_Status='YES') | Q(Approval_Status='NO'))
    # not_approved_materials = MaterialApproval.objects.filter(Approval_Status='NO')
    
    context = {
        "materials_for_approval": materials_for_approval,
        "approved_materials" : approved_materials,
        # "not_approved_materials" : not_approved_materials
    }
    
    return render(request, 'FileApp/admin_material_approval.html', context)


# def download_request(request):
#     return render(request, 'FileApp/Download.html')
    
    

def user_download_requests(request):
    
    download_material_requests = MaterialApproval.objects.filter(Requested_User=request.user)
    context = {
        "download_material_requests": download_material_requests
    }
    return render(request, 'FileApp/user_download_requests.html', context)


def view_all_data(request):
    print("Inside View Data View")
    All_data = Material.objects.all()
    print("All Data : " , All_data)
    return render(request, 'FileApp/NewFile.html')