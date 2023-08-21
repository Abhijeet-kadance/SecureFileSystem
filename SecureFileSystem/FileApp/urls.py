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
    path('dashboard',views.dashboard_view,name='dashboard'),
]
