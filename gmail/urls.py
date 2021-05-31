from django.urls import path
from gmail import views
#
urlpatterns=[
    path('',views.main,name='main'),
#     path('login_request/',views.login_request,name='login_request'),
#     path('login_validate/',views.login_validate,name='login_validate'),
]