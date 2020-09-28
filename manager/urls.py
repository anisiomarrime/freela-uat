"""mozpexels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'manager'

urlpatterns = [
    # Utilizando o {id} para buscar o objeto
    path('', IndexTemplateView.as_view(), name='index_manager'),

    path('rewards/', RewardTemplateView.as_view(), name='rewards'),

    path('bugs/', BugTemplateView.as_view(), name='bugs'),

    path('account/verify/', AccountVerifyTemplate.as_view(), name='verify'),

    path('payments/', PaymentsTemplate.as_view(), name='payments'),

    path('api/v1/approve/<int:id>/', AccountVerifyTemplate.verify, name='approve')
]