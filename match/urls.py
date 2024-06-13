"""
URL configuration for cupofjoe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include

from . import views

app_name = 'match'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),

    # Stable marriage page
    path('stable_marriage/', views.stable_marriage, name='stable_marriage'),
    path('sm_matching/', views.sm_matching, name='sm_matching'),
    path('sm_matching_suitors/', views.sm_matching_suitors, name='sm_matching_suitors'),
    path('sm_matching_reviewers/', views.sm_matching_reviewers, name='sm_matching_reviewers'),
    path('sm_matching_complete/', views.sm_matching_complete, name='sm_matching_complete'),

    # Stable roommate page
    path('stable_roommate/', views.stable_roommate, name='stable_roommate'),

    # Boehmer & Heeger page
    path('boehmer_heeger/', views.boehmer_heeger, name='boehmer_heeger'),
]