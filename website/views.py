import uuid
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, render_to_response
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView
from django.contrib.auth import logout, login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from validate_email import validate_email

from mozlancers.models import Freelancer, Category, Project, Employer, Skill, Budget, ExperienceLevel, Proposal, \
    LiterarySkills, Package, ProjectInvite, UserToken, FreelancerStats, Chat, City, Notification, BugReport, Reward, \
    BugType, Status, Newsletter, FreelaGateway, PaymentMethod, PaymentPackage
from .forms import FormLogin, FormEmployerProfile, FormEmployerProject, \
    FormFreelancerSearch, FormProjectSearch, FormUserRegister

from mozlancers.tokens import PasswordResetTokenGenerator

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


MAX_RESULTS_DASHBOARD = 4
MAX_RESULTS_DEFAULT = 6

def send_email(msg, sub, to):
    message = Mail(from_email='noreply@freela.co.mz', to_emails=to, subject=sub, html_content=msg)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        return 500

def load_photo(request):
    if not None == request.user.id:
        total_news = Notification.objects.filter(target=request.user, is_opened=0).count()

        user = request.user
        freela = Freelancer.objects.get(user=user)

        user.is_notification = total_news > 0

        if freela.is_main == 1:
            request.user.photo = freela.photo
        else:
            employer = Employer.objects.get(user=user)
            request.user.photo = employer.photo

def paginate(values, max=MAX_RESULTS_DEFAULT, page=1):
    paginator = Paginator(values, max)
    try:
        page = int(str(page).replace('#', ''))
        values = paginator.page(page)
    except PageNotAnInteger:
        values = paginator.page(1)
    except EmptyPage:
        values = paginator.page(paginator.num_pages)
    return values

class AccountTemplateView(TemplateView):
    template_name = "change_password.html"
    context_object_name = "change_password"

    def verify(request):
        load_photo(request)
        return render(request, "verify_account.html")

    def change_password(request):
        if request.method == 'GET':
            try:
                token = request.GET['token']
                tokenGenerator = PasswordResetTokenGenerator()
                userToken = UserToken.objects.get(token=token)
                is_valid = tokenGenerator.check_token(userToken.user, userToken.token)

                if is_valid:
                    return render(request, "change_password.html", {'token': token})
                else:
                    return redirect('/login/')
            except:
                return render(request, "change_password.html")

        if request.method == 'POST':
            userToken = UserToken.objects.get(token=request.GET['token'])
            user = User.objects.get(id=userToken.user.id)
            if request.POST['new_password']:
                user.password = make_password(request.POST['new_password'])
                user.save()
                return redirect('/login/')
            else:
                return render(request, "change_password.html")

    def privacy_policy(request):
        load_photo(request)
        return render(request, "privacy_policy.html")


class IndexTemplateView(TemplateView):
    template_name = "index.html"
    context_object_name = "index"

    def get_context_data(self, filter=None, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        freelancers = Freelancer.objects.filter(status=1).order_by("-exp")[:3]
        projects = Project.objects.filter(is_exclusive=False)
        projects = projects.filter(status=Status.objects.get(id=4)).order_by("-id")[:3]

        for project in projects:
            project.project_skills = project.skills.all()

        for freelancer in freelancers:
            freelancer.lancer_skills = freelancer.skills.all()

        context['freelancers'] = freelancers
        context['projects'] = projects
        context['total_p'] = Project.objects.filter(is_exclusive=False).count()
        return context

    def get(self, request, **kwargs):
        context = IndexTemplateView.get_context_data(self, **kwargs)
        context['categories'] = Category.objects.all()
        context['budgets'] = Budget.objects.all()
        context['top_categories'] = Category.objects.order_by("id")[:3]
        load_photo(request)

        return render(request, 'index.html', context)

    def post(self, request, **kwargs):
        context = IndexTemplateView.get_context_data(self, **kwargs)
        context['categories'] = Category.objects.all()
        context['budgets'] = Budget.objects.all()
        context['top_categories'] = Category.objects.order_by("id")[:3]
        load_photo(request)

        try:
            if validate_email(request.POST['email']):
                Newsletter.objects.create(email=request.POST['email'])
                context['message'] = 'O seu e-mail foi adicionado com sucesso!'
                context['severity'] = 'success'
        except:
            context['message'] = 'O seu e-mail já foi adicionado!'
            context['severity'] = 'warning'
            pass

        return render(request, 'index.html', context)


class LoginTemplateView(TemplateView):
    template_name = "login.html"
    context_object_name = "login"

    def get(self, request, **kwargs):
        form = FormLogin(request.GET)
        if form.is_valid():
            user = authenticate(username=form.data['email'], password=form.data['password'])

            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            return render(request, "login.html")


class LogoutTemplateView(TemplateView):
    template_name = "login.html"
    context_object_name = "login"

    def get(self, request, **kwargs):
        logout(request)
        return redirect('/')


class RegisterConfirmationTemplateView(TemplateView):
    template_name = "register_confirmation.html"
    context_object_name = "register_confirmation"
    
    def get(self, request, **kwargs):
        token = request.GET['token']
        try:
            token = UserToken.objects.get(token=token)
            user = token.user
            user.is_active = True
            user.save()
            return render(request, "register_confirmation.html",
                          {'user': user, 'is_freelancer': Freelancer.objects.get(user=user).is_main})
        except:
            return redirect("/invalid_token/")


class RegisterTemplateView(TemplateView):
    template_name = "register.html"
    context_object_name = "register"

    def get(self, request, **kwargs):
        try:
            apply = request.GET['apply']
            return render(request, "register.html", {'apply': apply})
        except:
            return render(request, "register.html")

    def post(self, request):
        apply = request.GET['apply']
        response = {"message": "", "severity": ""}
        form = FormUserRegister(request.POST)

        if form.is_valid():
            if validate_email(form.data['email']):
                try:
                    User.objects.get(email=form.data['email'])
                    response["message"] = 'Já existe uma conta com este e-mail.'
                    response["severity"] = 'warning'
                except:
                    data = form.data
                    user = User.objects.create_user(email=data['email'], username=data['email'], password=data['password'],
                                                    is_active=False)

                    name = str(data['name']).split(' ')
                    user.first_name = name[0]
                    user.last_name = str(data['name']).replace(name[0], "").strip()
                    user.save()

                    Employer.objects.create(slug=slugify(name), user=user, name=data['name'], is_main=False if apply == 'w' else True)
                    freelancer = Freelancer.objects.create(slug=slugify(name), user=user, city=City.objects.get(id=1),is_main=False if apply == 'h' else True, stats=FreelancerStats.objects.create())

                    tokenGenerator = PasswordResetTokenGenerator()
                    token = tokenGenerator.make_token(user)
                    UserToken.objects.create(token=token, user=user)

                    res = send_email('<h5>Olá {},</h5><p>Seja bem-vindo(a) ao Freela!</p><p>Para começar sua Carreira no Freela, activa sua conta no seguinte link: https://www.freela.co.mz/register/confirmation?token={}</p>'.format(user.first_name, token), "Active sua conta no Freela🔓", user.email)

                    if res == 500:
                        send_email(
                            '<h5>Olá {},</h5><p>Seja bem-vindo(a) ao Freela!</p><p>Para começar sua Carreira no Freela, activa sua conta no seguinte link: https://www.freela.co.mz/register/confirmation?token={}</p>'.format(
                                user.first_name, token), "Active sua conta no Freela🔓", user.email)

                    try:
                        freelancer.skills.add(Skill.objects.get(id=1))
                        freelancer.save()
                    except:
                        pass

                    return render(request, "register.html", {'message': "", 'form': form.data, 'apply': 'c'})
            else:
                response["message"] = "Por favor digite um endereço de email válido, o seu email não foi encontrado."
                response["severity"] = 'error'
        else:
            response["message"] = "Por favor preencha devidamente os campos."
            response["severity"] = 'error'
        return render(request, "register.html", {'response': response, 'form': form.data, 'apply': apply})


class CandidateDashboardTemplateView(TemplateView):
    template_name = "freelancer-dashboard.html"
    context_object_name = "freelancer-dashboard"

    def get(self, request, **kwargs):
        page = request.GET.get('page', 1)
        load_photo(request)

        try:
            freelancer = Freelancer.objects.get(user=request.user.id)
            literary_skills = LiterarySkills.objects.filter(freelancer=freelancer)
            freelancer.lancer_skills = freelancer.skills.all()

            total_proposals = '0'
            total_invites = '0'
            invites = []
            proposals = []

            if request.user.id:
                total_proposals = str(Proposal.objects.filter(freelancer=freelancer).count())
                total_invites = ProjectInvite.objects.filter(freelancer=freelancer).count()
                proposals = Proposal.objects.filter(freelancer=Freelancer.objects.get(user=request.user)).order_by(
                    "-id")
                invites = ProjectInvite.objects.filter(freelancer=Freelancer.objects.get(user=request.user)).order_by(
                    "-id")

                proposals = paginate(proposals, MAX_RESULTS_DASHBOARD, page)

                invites = paginate(invites, MAX_RESULTS_DASHBOARD, page)

            skills = Skill.objects.all()
            for skill in skills:
                for f_skill in freelancer.lancer_skills:
                    if skill.id == f_skill.id:
                        skill.is_selected = True
                        break

            freelancer.payments = FreelaGateway.objects.filter(freelancer=freelancer)

            projects_on = Proposal.objects.filter(freelancer=freelancer, status=Status.objects.get(id=2))
            invites_on = ProjectInvite.objects.filter(freelancer=freelancer, status=Status.objects.get(id=2))

            total_projects_on = len(invites_on) + len(projects_on)

            context = {'total_invites': total_invites, 'total_projects_on': total_projects_on, 'invites_on': invites_on, 'projects_on': projects_on, 'proposals': proposals, 'invites': invites, 'total_proposals': total_proposals,
                       'form': freelancer, 'categories': Category.objects.all, 'packages': Package.objects.all(),
                       'skills': skills, 'literary_skills': literary_skills, 'cities': City.objects.all(), 'payment_methods': PaymentMethod.objects.all()}
            return render(request, "freelancer-dashboard.html", context)
        except Exception as e:
            print(e)
            return redirect('/login/')


class FreelancerTemplateView(TemplateView):
    template_name = "freelancer.html"
    context_object_name = "freelancer"

    def view(request, slug):
        load_photo(request)
        my_projects = []

        if request.user.id:
            my_projects = Project.objects.filter(employer=Employer.objects.get(user=request.user))

        try:
            freelancer = Freelancer.objects.get(slug=slug)
        except:
            return redirect('/freelancers/?query=&address=&speciality=')

        proposals = Proposal.objects.filter(freelancer=freelancer)

        freelancer.lancer_skills = freelancer.skills.all()
        freelancer.literary_skills = LiterarySkills.objects.filter(freelancer=freelancer)
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
                 'Outubro', 'Novembro', 'Dezembro']

        for l_skill in freelancer.literary_skills:
            l_skill.month = meses[l_skill.month - 1]

        freelancer.stats.proposals_sent = Proposal.objects.filter(freelancer=freelancer, status=Status.objects.get(id=3)).count()
        freelancer.stats.projects_con = proposals.filter(status=Status.objects.get(id=2)).count()
        freelancer.stats.projects_end = proposals.filter(status=Status.objects.get(id=6)).count()

        last_seen = get_timed(freelancer.user.last_login)
        member_since = get_timed(freelancer.user.date_joined)

        return render(request, "freelancer.html", {'last_seen': last_seen, 'member_since': member_since, 'budgets': Budget.objects.all(), 'categories': Category.objects.all, 'my_projects': my_projects, 'freelancer': freelancer})


class FreelancersTemplateView(TemplateView):
    template_name = "freelancer.html"
    context_object_name = "freelancer"

    def get(self, request, **kwargs):
        load_photo(request)
        page = request.GET.get('page', 1)
        form = FormFreelancerSearch(request.GET)
        query = Q(job_title__contains=form.data['query'])
        my_projects = []
        # 258875322233
        if len(form.data['query']) >= 1:
            query.add(Q(skills__name__contains=form.data['query']), Q.OR)

        if len(form.data['speciality']) >= 1:
            speciality = Category.objects.get(name=form.data['speciality'])
            query.add(Q(speciality=speciality.id), Q.AND)

        if len(form.data['address']) >= 1:
            query.add(Q(address__contains=form.data['address']), Q.AND)

        query.add(Q(status=1), Q.AND)

        freelancers = Freelancer.objects.filter(query).order_by("-exp").distinct()

        for freelancer in freelancers:
            freelancer.lancer_skills = freelancer.skills.all()

        freelancers = paginate(freelancers, MAX_RESULTS_DEFAULT, page)

        return render(request, "freelancers.html",
                      {'budgets': Budget.objects.all(), 'freelancers': freelancers, 'categories': Category.objects.all,
                       'form': form.data})


class EmployerDashboardTemplateView(TemplateView):
    template_name = "employer-dashboard.html"
    context_object_name = "employer-dashboard"

    def post(self, request):
        load_photo(request)
        response = {"message": "Por favor preencha devidamente os campos, e tente novamente.", "severity": "error"}
        page = request.GET.get('page', 1)

        user = request.user
        form = FormEmployerProfile(request.POST)
        employer = Employer.objects.get(user=user)
        hiring = ProjectInvite.objects.filter(project__employer=employer)

        if form.is_valid():
            speciality = Category.objects.get(id=int(form.data['speciality']))
            employer.name = form.data['name']
            employer.speciality = speciality
            employer.overview = form.data['overview']
            employer.save()

            response = {"message": "O seu perfil foi actualizado com sucesso!", "error": False, "severity": "success"}

        form = FormEmployerProject(request.POST)

        if form.is_valid():
            form = form.data
            project = Project.objects.create(slug=slugify(form['title']), employer=Employer.objects.get(user=request.user.id), title=form['title'],
                                             category=Category.objects.get(id=int(form['category'])),
                                             experience=ExperienceLevel.objects.get(id=int(form['experience'])),
                                             budget=Budget.objects.get(id=int(form['budget'])),
                                             deadline=form['deadline'], overview=form['overview'])
            skills = request.POST.getlist('skills')
            for skill in skills:
                project.skills.add(Skill.objects.get(id=int(skill)))
            project.save()

            response = {"message": "O projecto foi publicado com sucesso!", "error": False, "severity": "success"}

        projects = Project.objects.filter(employer=employer)
        projects_on = Proposal.objects.filter(project__employer=employer, status=Status.objects.get(id=2))
        invites_on = ProjectInvite.objects.filter(project__employer=employer, status=Status.objects.get(id=2))

        total_project_on = len(projects_on) + len(invites_on)
        total_p = len(projects)
        total_h = len(hiring)

        hiring = paginate(hiring, MAX_RESULTS_DASHBOARD, page)
        projects = paginate(projects, MAX_RESULTS_DASHBOARD, page)

        context = {'projects_on': projects_on, 'total_project_on': total_project_on, 'invites_on': invites_on, 'hiring': hiring, 'total_h': total_h, 'total_p': total_p, 'response': response, 'form': employer, 'categories': Category.objects.all, 'skills': Skill.objects.all, 'projects': projects}
        return render(request, "employer-dashboard.html", context)

    def get(self, request, **kwargs):
        load_photo(request)
        page = request.GET.get('page', 1)

        try:
            employer = Employer.objects.get(user=request.user.id)
            hiring = ProjectInvite.objects.filter(project__employer=employer)

            projects = Project.objects.filter(employer=employer)

            projects_on = Proposal.objects.filter(project__employer=employer, status=Status.objects.get(id=2))
            invites_on = ProjectInvite.objects.filter(project__employer=employer, status=Status.objects.get(id=2))

            total_project_on = len(projects_on) + len(invites_on)
            total_p = len(projects)
            total_h = len(hiring)

            hiring = paginate(hiring, MAX_RESULTS_DASHBOARD, page)
            projects = paginate(projects, MAX_RESULTS_DASHBOARD, page)

            context = {'projects_on': projects_on, 'total_project_on': total_project_on, 'invites_on': invites_on, 'hiring': hiring, 'total_p': total_p, 'total_h': total_h, 'form': employer, 'categories': Category.objects.all,
                       'skills': Skill.objects.all, 'budgets': Budget.objects.all, 'experiences': ExperienceLevel.objects.all,
                       'packages': Package.objects.all(), 'projects': projects}
            return render(request, "employer-dashboard.html", context)
        except Exception as e:
            return redirect('/login/')


class EmployerTemplateView(TemplateView):
    template_name = "employer.html"
    context_object_name = "employer"

    def view(request, id):
        load_photo(request)
        employer = Employer.objects.get(id=id)
        projects = Project.objects.filter(employer=employer.id)
        total_projects = len(projects)
        total_done = projects.filter(status=6).count()
        return render(request, "employer.html",
                      {'total_done': total_done, 'total_projects': total_projects, 'employer': employer, 'projects': Project.objects.filter(employer=employer.id, status=4, is_exclusive=False)})


class ProjectsTemplateView(TemplateView):
    template_name = "projects.html"
    context_object_name = "projects"

    def get(self, request, **kwargs):
        load_photo(request)
        form = FormProjectSearch(request.GET)
        query = Q(title__contains=form.data['query'])
        page = request.GET.get('page', 1)

        if len(form.data['speciality']) >= 1:
            speciality = Category.objects.get(name=form.data['speciality'])
            query.add(Q(category=speciality.id), Q.AND)

        try:
            if len(form.data['budget']) >= 1:
                budget = Budget.objects.get(id=form.data['budget'])
                query.add(Q(budget=budget.id), Q.AND)
        except MultiValueDictKeyError:
            pass

        try:
            if len(form.data['experience']) >= 1:
                experience = ExperienceLevel.objects.get(id=form.data['experience'])
                query.add(Q(experience=experience.id), Q.AND)
        except MultiValueDictKeyError:
            pass

        query.add(Q(is_exclusive=False), Q.AND)
        query.add(Q(status=Status.objects.get(id=4)), Q.AND)

        projects = Project.objects.filter(query)
        for project in projects:
            project.project_skills = project.skills.all()[:1]

        projects = paginate(projects, MAX_RESULTS_DEFAULT, page)

        return render(request, "projects.html",
                      {'projects': projects, 'categories': Category.objects.all, 'budgets': Budget.objects.all,
                       'experiences': ExperienceLevel.objects.all(), 'form': form.data})


class ProjectTemplateView(TemplateView):
    template_name = "project.html"
    context_object_name = "project"

    def view(request, id):
        load_photo(request)
        project = Project.objects.get(id=id)
        project.project_skills = project.skills.all()
        is_owner = False

        try:
            employer = Employer.objects.get(user=request.user)
            if employer == project.employer:
                is_owner = True
        except:
            is_owner = False

        proposals = Proposal.objects.filter(project=project)

        for proposal in proposals:
            proposal.updated_at = get_timed(proposal.created_at)

        return render(request, "project.html",
                      {'is_owner': is_owner, 'project': project, 'proposals': proposals})


class PlansCheckoutTemplateView(TemplateView):
    template_name = "plans_checkout.html"
    context_object_name = "plans_checkout"

    def view(request, id):
        load_photo(request)
        plan = Package.objects.get(id=id)
        if plan.id == 1:
            return redirect('/checkout/completed/?tk=' + str(plan.id))
        return render(request, "plans_checkout.html", {'plan': plan})


class PlansTemplateView(TemplateView):
    template_name = "plans.html"
    context_object_name = "plans"

    def get(self, request, **kwargs):
        load_photo(request)
        plans = Package.objects.all()
        try:
            for plan in plans:
                plan.all_features = plan.features.all()
            package = Freelancer.objects.get(user=request.user).package.id
            return render(request, "plans.html", {'plans': plans, 'current_package': package})
        except:
            redirect('/login')


class CheckoutCompletedTemplateView(TemplateView):
    template_name = "checkout_completed.html"
    context_object_name = "checkout_completed"

    def get(self, request, **kwargs):
        load_photo(request)
        payment = PaymentPackage.objects.get(token=request.GET['tk'])
        payment.is_completed = True

        freelancer = Freelancer.objects.get(user=payment.user)
        employer = Employer.objects.get(user=payment.user)

        freelancer.package = payment.package
        employer.package = payment.package

        if payment.package.is_premium:
            freelancer.exp = freelancer.exp + 10
        else:
            freelancer.exp = freelancer.exp + 1

        freelancer.save()
        employer.save()
        payment.save()

        return render(request, "checkout_completed.html", {'name': request.user.first_name, 'package': payment.package.name})


class InvalidTokenTemplateView(TemplateView):
    template_name = "invalid_token.html"
    context_object_name = "invalid_token"


class FeedbackTemplateView(TemplateView):
    template_name = "feedback.html"
    context_object_name = "feedback"

    def get(self, request, **kwargs):
        load_photo(request)
        query = request.GET.get('search', -1)
        if query == -1:
            bugs = BugReport.objects.all()
        else:
            query = str(query).replace('#', '')
            if query.isnumeric():
                bugs = BugReport.objects.filter(id=int(query))
            else:
                bugs = BugReport.objects.filter(title__contains=query)

        for bug in bugs:
            bug.updated_at = get_timed(bug.created_at)

        page = request.GET.get('page', 1)
        bugs = paginate(bugs, MAX_RESULTS_DEFAULT, page)

        total_bugs = BugReport.objects.count()
        bug_fixed = BugReport.objects.filter(status=2).count()
        last_reward = Reward.objects.last()
        bug_types = BugType.objects.all()
        return render(request, "feedback.html", {'query': query, 'bugs': bugs, 'total_bugs': total_bugs, 'bug_fixed': bug_fixed, 'last_reward': last_reward, 'bug_types': bug_types})


class NotificationsTemplateView(TemplateView):
    template_name = "notifications.html"
    context_object_name = "notifications"

    def get(self, request, **kwargs):
        load_photo(request)
        try:
            notifications = Notification.objects.filter(target=request.user).order_by("-id")[:5]
            total_news = Notification.objects.filter(target=request.user, is_opened=0).count()

            for notification in notifications:
                notification.is_opened = 1
                notification.save()
                notification.updated_at = get_timed(notification.created_at)
            return render(request, "notifications.html", {'total_news': total_news, 'notifications': notifications})
        except Exception as e:
            print(e)
            return redirect('/login')


class HireConfirmationTemplateView(TemplateView):
    template_name = "hire_confirmation.html"
    context_object_name = "hire_confirmation"

    def view(request, id):
        load_photo(request)
        try:
            proposal = Proposal.objects.get(id=int(id))
            freelancer = proposal.freelancer
            freelancer.payments = FreelaGateway.objects.filter(freelancer=freelancer)
            employer = proposal.project.employer

            projects_on = Project.objects.filter(employer=employer, status=Status.objects.get(id=2)).count()

            if employer.package.max_project <= projects_on:
                return render(request, "hire_status.html", {'employer': employer})
            else:
                return render(request, "hire_confirmation.html", {'freelancer': freelancer, 'proposal': proposal})
        except Exception as e:
            print(e)
            return redirect("/")

    def invite(request, id):
        load_photo(request)
        try:
            invite = ProjectInvite.objects.get(id=int(id))
            freelancer = invite.freelancer
            if invite.status.id == 7:
                freelancer.payments = FreelaGateway.objects.filter(freelancer=freelancer)
                return render(request, "hire_confirmation.html", {'freelancer': freelancer, 'proposal': invite})
            else:
                return redirect("/")
        except Exception as e:
            print(e)
            return redirect("/")

    def confirm_hire(request, id):
        proposal = Proposal.objects.get(id=int(id))
        project = Project.objects.get(id=proposal.project.id)

        project.status = Status.objects.get(id=2)
        proposal.status = Status.objects.get(id=2)
        proposal.save()
        project.save()

        # Save and Notify other Freelas
        proposals = Proposal.objects.filter(project=project)
        for prop in proposals:
            if prop.id == proposal.id:
                Notification.objects.create(user=request.user, target=proposal.freelancer.user,
                                            title='Proposta',
                                            description='a sua proposta para o projecto #' + project.title + ' foi aceite.')
            else:
                prop.status = Status.objects.get(id=8)
                prop.save()
                Notification.objects.create(user=request.user, target=proposal.freelancer.user,
                                            title='Proposta', description='a sua proposta para o projecto #' + project.title + ' não teve êxito.')

        response = {"message": "A proposta foi confirmada, sucessos com o projecto!", "error": False}
        return JsonResponse(response)

    def confirm_invite(request, id):
        invite = ProjectInvite.objects.get(id=int(id))
        project = Project.objects.get(id=invite.project.id)

        project.status = Status.objects.get(id=2)
        invite.status = Status.objects.get(id=2)

        # Save and Notify other Freelas
        invites = ProjectInvite.objects.filter(project=project)
        for prop in invites:
            if prop.id == invite.id:
                Notification.objects.create(user=request.user, target=prop.freelancer.user,
                                            title='Proposta',
                                            description='a sua proposta para o projecto #' + project.title + ' foi aceite.')
            else:
                prop.status = Status.objects.get(id=8)
                prop.save()
                Notification.objects.create(user=request.user, target=prop.freelancer.user,
                                            title='Proposta', description='a sua proposta para o projecto #' + project.title + ' não teve êxito.')

        invite.save()
        project.save()
        response = {"message": "A proposta foi confirmada, sucessos com o projecto!", "error": False}
        return JsonResponse(response)


class FAQTemplateView(TemplateView):
    template_name = "faq.html"
    context_object_name = "faq"


def get_timed(data):
    SEC = 60
    DAY = 24
    WEK = 7
    MON = 4
    des = 'segundo'
    fmt = '%Y-%m-%d %H:%M:%S'
    dt1 = datetime.strptime(data.strftime(fmt), fmt)
    dt2 = datetime.now()
    # Output in secounds
    val = (dt2-dt1).total_seconds() * SEC / 60
    # Output in minutes
    if val > SEC:
        val = val / SEC
        des = 'minuto'
    if val > SEC and des == 'minuto':
        val = val / SEC
        des = 'hora'
    if val > DAY and des == 'hora':
        val = val / DAY
        des = 'dia'
    if val > WEK and des == 'dia':
        val = val / WEK
        des = 'semana'
    if val > MON and des == 'semana':
        val = val / MON
        des = 'mês'
    val = int(val)
    # Singular/Plural
    if val > 1:
        if des == 'mês': des = des+'e'
        des = des + 's'
    return [val, des]