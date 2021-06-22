# -*- coding: utf-8 -*-

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="what-index"),

    path('browse/', browse, name="what-browse"),

    path('composers/', composers, name="what-composers"),
    path('composers/<int:composer_id>', composer_details, name="what-composer_details"),
    path('composers/<int:composer_id>-<slug:slug>', composer_details, name="what-composer_details"),

    path('works/', works, name="what-works"),
    path('works/<int:work_id>', work_details, name="what-work_details"),
    path('work/<int:work_id>', work_details, name="what-work_details"),

    path('search/', search, name="what-search"),




    path('check/<int:start>-<int:end>', check, name="what-check"),

    path('mass/', create_mass_work_version, name="what-create-mass-work-version"),

]