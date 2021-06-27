# -*- coding: utf-8 -*-

from django.urls import path
from .views import *

urlpatterns = [
    path('composers/', search_composers, name="api-composers"),

    path('instruments/', search_instruments, name="api-instruments"),

]
