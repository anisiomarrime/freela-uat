from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from mozlancers.models import Freelancer, BugReport, Notification, PaymentPackage


class IndexTemplateView(TemplateView):
    template_name = "index_manager.html"
    context_object_name = "index_manager"

    def get_context_data(self, filter=None, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = IndexTemplateView.get_context_data(self, **kwargs)

        if None == request.user.id:
            return redirect('/')

        context['total_budget'] = PaymentPackage.objects.filter(is_completed=True).aggregate(Sum('amount'))['amount__sum']
        context['total_freelas'] = Freelancer.objects.count()
        context['total_bugs'] = BugReport.objects.count()
        return render(request, 'index_manager.html', context)

class BugTemplateView(TemplateView):
    template_name = "bugs.html"
    context_object_name = "bugs"

    def get_context_data(self, filter=None, **kwargs):
        context = super(BugTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = BugTemplateView.get_context_data(self, **kwargs)
        return render(request, 'bugs.html', context)


class RewardTemplateView(TemplateView):
    template_name = "rewards.html"
    context_object_name = "rewards"

    def get_context_data(self, filter=None, **kwargs):
        context = super(RewardTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = RewardTemplateView.get_context_data(self, **kwargs)
        return render(request, 'rewards.html', context)


class AccountVerifyTemplate(TemplateView):
    template_name = "admin_verify_account.html"
    context_object_name = "admin_verify_account"

    def get_context_data(self, filter=None, **kwargs):
        context = super(AccountVerifyTemplate, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = AccountVerifyTemplate.get_context_data(self, **kwargs)

        if None == request.user.id:
            return redirect('/')

        context['freelancers'] = Freelancer.objects.all()
        return render(request, 'admin_verify_account.html', context)

    def verify(request, id):
        user = User.objects.get(id=Freelancer.objects.get(id=int(id)).user.id)
        user.is_staff = 1
        user.save()
        Notification.objects.create(user=request.user, target=user, title='Account',
                                    description='a sua identidade foi verificada.')

        return JsonResponse(status=200, data={'user': user.id})


class PaymentsTemplate(TemplateView):
    template_name = "payments.html"
    context_object_name = "payments"

    def get_context_data(self, filter=None, **kwargs):
        context = super(PaymentsTemplate, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = PaymentsTemplate.get_context_data(self, **kwargs)

        if None == request.user.id:
            return redirect('/')

        context['payments'] = PaymentPackage.objects.all()
        return render(request, 'payments.html', context)