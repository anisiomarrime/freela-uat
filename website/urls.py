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

from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

from .views import IndexTemplateView, CandidateDashboardTemplateView, EmployerDashboardTemplateView, LoginTemplateView, \
    LogoutTemplateView, FreelancerTemplateView, EmployerTemplateView, FreelancersTemplateView, ProjectsTemplateView, \
    ProjectTemplateView, AccountTemplateView, PlansTemplateView, RegisterTemplateView, \
    PlansCheckoutTemplateView, CheckoutCompletedTemplateView, RegisterConfirmationTemplateView, \
    InvalidTokenTemplateView, NotificationsTemplateView, FeedbackTemplateView, HireConfirmationTemplateView

from .api_views import *

app_name = 'website'


urlpatterns = [

    path('login_register/', login_register, name='login_register'),

    # Utilizando o {slug} para buscar o objeto
    path('proposal/', proposal, name='proposal'),

    path('project/', project, name='project'),

    # Utilizando o {slug} para buscar o objeto
    path('params/', params, name='params'),

    # Utilizando o {slug} para buscar o objeto
    path('upload_foto/', upload_foto, name='upload_foto'),

    # Utilizando o {slug} para buscar o objeto
    path('load_foto/<filename>', load_foto, name='load_foto'),

    # Utilizando o {slug} para buscar o objeto
    path('login/', LoginTemplateView.as_view(), name='login'),

    path('invalid_token/', InvalidTokenTemplateView.as_view(), name='invalid_token'),

    path('register/', RegisterTemplateView.as_view(), name='register'),

    path('register/confirmation', RegisterConfirmationTemplateView.as_view(), name='register_confirmation'),

    # Utilizando o {slug} para buscar o objeto
    path('reset_password/', reset_password, name="reset_password"),

    # Utilizando o {slug} para buscar o objeto
    path('accounts/change_password/', AccountTemplateView.change_password, name="account_change_password"),

    # Utilizando o {slug} para buscar o objeto
    path('account/verify/', AccountTemplateView.verify, name="account_verify"),

    path('about/privacy-policy/', AccountTemplateView.privacy_policy, name="privacy_policy"),

    path('api/v1/save_profile/', save_profile, name='save_profile'),

    path('api/v1/change_password/', change_password, name="change_password"),

    path('api/v1/add_literary/', literary_skill, name="literary_skill"),

    path('api/v1/technical_skill/', technical_skill, name="technical_skill"),

    path('api/v1/send_payment/', send_payment, name="send_payment"),

    path('api/v1/project_invite/', project_invite, name='project_invite'),

    path('api/v1/bug_report/', bug_report, name='bug_report'),

    path('api/v1/review/', review, name='review'),

    # Utilizando o {slug} para buscar o objeto
    path('logout/', LogoutTemplateView.as_view(), name='logout'),

    # Utilizando o {id} para buscar o objeto
    path('', IndexTemplateView.as_view(), name='index'),

    # Utilizando o {slug} para buscar o objeto
    path('freelancer-dashboard/', CandidateDashboardTemplateView.as_view(), name='freelancer-dashboard'),

    # Utilizando o {slug} para buscar o objeto
    path('freelancer/<slug:slug>/', FreelancerTemplateView.view, name='freelancer'),

    # Utilizando o {slug} para buscar o objeto
    path('freelancers/', FreelancersTemplateView.as_view(), name='freelancers'),

    # Utilizando o {slug} para buscar o objeto
    path('employer-dashboard/', EmployerDashboardTemplateView.as_view(), name='employer-dashboard'),

    # Utilizando o {slug} para buscar o objeto
    path('employer/<int:id>/', EmployerTemplateView.view, name='employer'),

    # Utilizando o {slug} para buscar o objeto
    path('projects/', ProjectsTemplateView.as_view(), name='projects'),

    # Utilizando o {slug} para buscar o objeto
    path('employer_projects/', employer_projects, name='employer_projects'),

    # Utilizando o {slug} para buscar o objeto
    path('project/<int:id>/', ProjectTemplateView.view, name='project'),

    # Utilizando o {slug} para buscar o objeto
    path('plans/', PlansTemplateView.as_view(), name='plans'),

    path('plans/checkout/<int:id>/', PlansCheckoutTemplateView.view, name='plans_checkout'),

    path('checkout/completed/', CheckoutCompletedTemplateView.as_view(), name='messages'),

    path('notifications/', NotificationsTemplateView.as_view(), name='notifications'),

    path('feedback/', FeedbackTemplateView.as_view(), name='feedback'),

    path('email/', categorias, name='email'),

    path('project/hire/<int:id>/', HireConfirmationTemplateView.view, name='hire_confirmation'),

    path('project/invite/<int:id>/', HireConfirmationTemplateView.invite, name='invite_confirmation'),

    path('api/v1/proposal/confirm/<int:id>/', HireConfirmationTemplateView.confirm_hire, name='confirm_hire'),

    path('api/v1/invite/confirm/<int:id>/', HireConfirmationTemplateView.confirm_invite, name='confirm_invite'),

    path('api/v1/feela_payments/', payment_method, name='payment_method')
]