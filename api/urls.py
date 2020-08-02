from django.contrib import admin
from django.urls import path
from api.views import *
import datetime
urlpatterns =[
    path('login/',login),
    path('signup/',signup),
    path('transact/',transact),
    path('get_transaction',get_transaction),
    path('get_friends',get_friends),
    path('get_recent_shop',get_recent_shop),
    path('get_recent_student',get_recent_student),
    path('get_balance',get_balance),
    path('add_friend',add_friend),
    path('put_request',put_request),
]