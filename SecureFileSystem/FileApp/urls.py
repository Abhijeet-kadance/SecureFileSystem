from django.contrib import admin
from django.urls import path,include
from django.urls import path, include, re_path as url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('',views.index),
    path('register',views.regiter_view,name='register_view'),
    path('activate/<uid64>/<token>',views.user_activate_view,name='user_activate'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('dashboard',views.dashboard_view,name='dashboard'),
    path('captcha_refresh/', views.captcha_refresh, name='captcha_refresh'),  # added by shivam sharma
    path('change_password',views.change_password_view,name='change_password'),
    path('forgot_password',views.forgot_password_view,name='forgot_password'),
    path('download',views.download_view,name='download'),
    path('admin_material_approval',views.admin_material_approval,name='admin_material_approval'),
    path('user_download_requests',views.user_download_requests,name='user_download_requests'),
]
