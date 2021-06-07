# -*- coding: utf-8 -*-

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="what-index"),

    path('browse/', browse, name="what-browse"),

    path('composers/', browse_composers, name="what-composers"),
    path('composers/<int:composer_id>', browse_composer_details, name="what-browse_composer_details"),
    path('composer/<int:composer_id>', browse_composer_details, name="what-browse_composer_details"),

    path('works/', browse_works, name="what-browse"),
    path('works/<int:work_id>', browse_work_details, name="what-browse-work-details-"),
    path('work/<int:work_id>', browse_work_details, name="what-browse-work-details-"),

    path('search/', search, name="what-search"),




    path('check/<int:start>-<int:end>', check, name="what-check"),

    path('mass/', create_mass_work_version, name="what-create-mass-work-version"),

]