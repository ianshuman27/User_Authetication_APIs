from django.contrib import admin
from django.urls import path
from . import views
from users.views import Register, Login, Userview, Logoutview, Refereshtoken

urlpatterns=[

   path('register/', Register.as_view(), name='signup'),
    path('login/', Login.as_view(), name='signin'),
     path('userview/', Userview.as_view(), name='viewuser'),
     path('logout/', Logoutview.as_view(), name='singout'),
     path('refresh/',Refereshtoken.as_view(), name='Refresh')
]