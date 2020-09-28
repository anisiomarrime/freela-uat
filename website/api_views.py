import uuid
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sendgrid import Mail, SendGridAPIClient
import string

from mozlancers.models import Freelancer, Employer, Category, Budget, Status, Project, Proposal, LiterarySkills, Skill, \
    Package, ProjectInvite, UserToken, FreelancerStats, City, ExperienceLevel, BugReport, BugType, FreelaGateway, \
    PaymentMethod, Notification, PaymentPackage
from .forms import FormLogin, FormUserRegister, FormProposalProject, FormLiterarySkills, FormProjectInvite, \
    FormFreelancerProfile, FormBugReport
from mozlancers.tokens import PasswordResetTokenGenerator

from django.http import JsonResponse, HttpResponse
from portalsdk import APIContext, APIMethodType, APIRequest


def send_email(msg, sub, to):
    message = Mail(from_email='noreply@freela.co.mz', to_emails=to, subject=sub, html_content=msg)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        return 500


@api_view(['GET'])
@csrf_exempt
def categorias(request):
    send_email(
        '<h5>Olá {},</h5><p>Seja bem-vindo(a) ao Freela!</p><p>Para começar sua Carreira no Freela, activa sua conta no seguinte link: https://www.freela.co.mz/register/confirmation?token={}</p>'.format(
            'Anisio', 'alkdjfPoejdklkmsdlkm'), "Active sua conta no Freela🔓", 'anisio.marrime@gmail.com')
    return JsonResponse(data={'status': 1}, status=201)

@api_view(['GET'])
@csrf_exempt
def params(request):
    experiences = ['Iniciante', 'Intermediário', 'Especialista']
    budgets = [{'minval': 0.00, 'maxval': 15000}, {'minval': 15000, 'maxval': 25000}, {'minval': 25000, 'maxval': 50000}]
    status = ['Aguardando Pagamento', 'Em Progresso', 'Aguardando Aprovação', 'Em Disputa', 'Cancelado', 'Concluído', 'Rejeitado', 'Fechado']

    """for ex in experiences:
        ExperienceLevel.objects.create(name=ex)"""

    for bg in budgets:
        Budget.objects.create(min_value=bg['minval'], max_value=bg['maxval'])

    for st in status:
        Status.objects.create(name=st)

    return JsonResponse({'status': 1}, status=201)

@api_view(['GET'])
@csrf_exempt
def load_foto(request, filename):
    image_data = open("uploads/"+filename, "rb").read()
    return HttpResponse(image_data, content_type="image/jpeg")

@api_view(['POST'])
@csrf_exempt
def upload_foto(request):
    pic = str(request.POST['foto'])

    tipo = str(request.POST['type'])

    if tipo == "1":
        freelancer = Freelancer.objects.get(user=request.user.id)
        freelancer.photo = pic
        if freelancer.photo == 'avatar.png':
            freelancer.exp = freelancer.exp + 5
        freelancer.save()
    else:
        employer = Employer.objects.get(user=request.user.id)
        employer.photo = pic
        employer.save()

    return JsonResponse({'status': 1}, status=201)


@api_view(['GET', 'POST'])
def login_register(request):
    response = {"message": request.method}

    if request.method == 'GET':
        form = FormLogin(request.GET)
        user = authenticate(username=form.data['email'], password=form.data['password'])

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Loggin Successfully!!!", "severity": "success"})
        else:
            try:
                user = User.objects.get(username=form.data['email'])
                if user.is_active == 1:
                    return JsonResponse({"message": "Username or Password incorrect!!", "severity": "info"})
                else:
                    return JsonResponse({"message": "Por favor verifique a sua conta, enviamos um e-mail de confirmação para seu endereço!", "severity": "info"})
            except Exception as e:
                return JsonResponse({"message": "Username or Password incorrect!!", "severity": "info"})

@api_view(['GET', 'POST'])
def proposal(request):
    response = {"message": "A sua Proposta foi enviada com sucesso!", "error": False,
                "severity": "success"}
    if request.method == 'POST':
        data = FormProposalProject(request.data)
        try:
            if data.is_valid():
                try:
                    data = FormProposalProject(request.data)
                    project = Project.objects.get(id=int(data['project'].value()))
                    freelancer = Freelancer.objects.get(user=request.user.id)
                    proposals = Proposal.objects.filter(Q(freelancer__id=freelancer.id), Q(project__id=project.id))

                    if len(proposals) >= 1:
                        response = {"message": "A sua Proposta já foi enviada para este Projecto, por favor aguarde pela resposta do Cliente.",
                                    "error": False,
                                    "severity": "info"}
                    else:
                        freelancer.exp = freelancer.exp + 2
                        Proposal.objects.create(project=project, freelancer=freelancer,
                                                budget=float(data['budget'].value()),
                                                deadline=int(data['deadline'].value()),
                                                description=data['description'].value())
                        Notification.objects.create(user=request.user, target=project.employer.user,
                                                    title='Proposta', description='enviou uma proposta para o projecto: #' + str(project.title))
                        freelancer.save()
                except Exception as e:
                    Proposal.objects.create(project=project, freelancer=freelancer, budget=float(data['budget'].value()), deadline=int(data['deadline'].value()), description=data['description'].value())
        except Exception as e:
            response = {"message": "Error interno: " + str(e), "error": True, "severity": "error"}
        return JsonResponse(response)

    if request.method == 'GET':
        action = request.GET['action']
        id = request.GET['id']
        try:
            p = Proposal.objects.get(id=int(id))
        except: pass

        if not None == request.user.id:
            if action == 'cl':
                p.status = Status.objects.get(id=5)
                p.save()
                Notification.objects.create(user=request.user, target=p.project.employer.user,
                                            title='Proposta', description='cancelou a proposta de ' + str(p.budget))
                return JsonResponse({"message": "A sua Proposta foi cancelada com sucesso!", "error": False,
                    "severity": "success"})
            if action == 'dl':
                p.delete()
                return JsonResponse({"message": "A sua Proposta foi eliminada com sucesso!", "error": False,
                    "severity": "success"})
            if action == 'ck':
                p.status = Status.objects.get(id=1)
                project = Project.objects.get(id=p.project.id)
                project.status = Status.objects.get(id=1)
                project.save()
                p.save()
                Notification.objects.create(user=request.user, target=p.project.employer.user,
                                            title='Proposta', description='concluiu o projecto: #' + p.project.title+', aguarda pela resposta.')
                return JsonResponse({"message": "O projecto foi concluido, aguarde pela resposta!", "error": False,
                                     "severity": "success"})

        return JsonResponse(status=404, data={'error': 'Sem permissao.'})

@api_view(['GET'])
def project(request):

    if request.method == 'GET':
        action = request.GET['action']
        id = request.GET['id']
        try:
            proj = Project.objects.get(id=int(id))
        except: pass

        if not None == request.user.id:
            if action == 'cl':
                proj.status = Status.objects.get(id=5)
                proj.save()
                #Notification.objects.create(user=request.user, target=p.project.employer.user, title='Proposta', description='cancelou o projecto: ' + str(p.title))
                return JsonResponse({"message": "O projecto foi cancelado com sucesso!", "error": False, "severity": "success"})

            if action == 'pd':
                prop = Proposal.objects.get(project=proj, status=Status.objects.get(id=1))
                prop.status = Status.objects.get(id=6)
                proj.status = Status.objects.get(id=6)

                Notification.objects.create(user=request.user, target=prop.freelancer.user,
                                            title='Projecto', description='colocou o projecto: #' + proj.title+' concluído.')

                proj.save()
                prop.save()
                return JsonResponse({"message": "O projecto foi concluido.", "error": False,
                                     "severity": "success"})

        return JsonResponse(status=404, data={'error': 'Sem permissao.'})

@api_view(['GET', 'POST'])
def project_invite(request):
    response = {"message": "Convite foi enviado com sucesso, por favor aguarde pela resposta do Freela.", "error": False, "severity": "success"}
    if request.method == 'POST':
        data = FormProjectInvite(request.data)
        try:
            if data.is_valid():
                freelancer = Freelancer.objects.get(id=int(data['freelancer'].value()))
                budget = Budget.objects.get(id=int(data['budget'].value()))
                category = Category.objects.get(id=int(data['category'].value()))

                if str(data['exclusive'].value()) == '1':
                    is_exclusive = False
                else:
                    is_exclusive = True

                project = Project.objects.create(slug=slugify(data['title'].value()), employer=Employer.objects.get(user=request.user.id),
                                                 title=data['title'].value(), category=category,
                                                 experience=ExperienceLevel.objects.get(id=1),is_exclusive=is_exclusive,
                                                 budget=budget, deadline=0, overview=data['description'].value())

                Notification.objects.create(user=request.user, target=freelancer.user, title='Proposta',
                                            description='enviou um convite para o projecto: #' + str(project.title))

                ProjectInvite.objects.create(freelancer=freelancer, project=project, status=Status.objects.get(id=3))
            else:
                response = {"message": "Não foi possível enviar o Convite, por favor preencha devidamente os campos.",
                            "error": False, "severity": "error"}
        except Exception as e:
            response = {"message": "Error interno: " + str(e), "error": True, "severity": "error"}
        return JsonResponse(response)

    if request.method == 'GET':
        action = request.GET['action']
        id = request.GET['id']
        try:
            proj_invite = ProjectInvite.objects.get(id=int(id))

            if not None == request.user.id:
                if action == 'cl':
                    proj_invite.status = Status.objects.get(id=5)
                    Notification.objects.create(user=request.user, target=proj_invite.freelancer.user, title='Convite',
                                                description='cancelou o convite do projecto: #' + str(
                                                    proj_invite.project.title))
                    proj_invite.created_at = now()
                    proj_invite.save()
                    return JsonResponse({"message": "O convite foi cancelado com sucesso!", "error": False, "severity": "success"})
                if action == 'rj':
                    proj_invite.status = Status.objects.get(id=8)
                    Notification.objects.create(user=request.user, target=proj_invite.freelancer.user,
                                                title='Convite', description='	rejeitou a sua proposta no projecto: #' + str(proj_invite.project.title))
                    proj_invite.created_at = now()
                    proj_invite.save()
                    return JsonResponse(
                        {"message": "O convite foi rejeitado com sucesso!", "error": False, "severity": "success"})
                if action == 'ck':
                    valor = str(request.GET['v'])

                    if valor.isnumeric():
                        proj_invite.status = Status.objects.get(id=7)
                        proj_invite.budget = Decimal(valor.replace(',', '.'))

                        user = request.user
                        freelancer = Freelancer.objects.get(user=user)

                        inv_on = ProjectInvite.objects.filter(freelancer=freelancer, status=Status.objects.get(id=2)).count()
                        prop_on = Proposal.objects.filter(freelancer=freelancer, status=Status.objects.get(id=2)).count()

                        if freelancer.package.max_project <= prop_on or freelancer.package.max_project <= inv_on:
                            return JsonResponse({"message": "Lamentamos, o seu pacote não permite executar mais de {} projecto(s) em simultâneo!".format(
                                         freelancer.package.max_project), "severity": "error", "error": True})

                        Notification.objects.create(user=request.user, target=proj_invite.project.employer.user,
                                                    title='Convite', description='enviou uma proposta para o convite do projecto: #' + str(
                                                        proj_invite.project.title))
                        proj_invite.created_at = now()
                        proj_invite.save()

                        return JsonResponse({"message": "A proposta foi enviada, aguarde a resposta.", "error": False,
                                             "severity": "success"})
                    else:
                        return JsonResponse({"message": "Por favor, envie um valor correcto!", "error": True,
                                             "severity": "error"})
        except:
            print('Error')

        return JsonResponse(status=404, data={'error': 'Sem permissao.'})

@api_view(['PUT', 'POST'])
def bug_report(request):
    response = {"message": "Bug foi enviado com sucesso, por favor aguarde pela resposta do Freela.", "error": 0, "severity": "success"}
    if request.method == 'POST':
        data = FormBugReport(request.data)
        try:
            if data.is_valid():
                data = data.data
                print(data)
                try:
                    bug_type = BugType.objects.get(id=int(data['type']))
                    BugReport.objects.create(user=request.user, bug_type=bug_type, title=data['title'],
                                         url=data['url'], description=data['description'])
                except Exception as e:
                    response = {"message": "Error interno: " + str(e), "error": 1, "severity": "error"}
            else:
                response = {"message": "Não foi possível enviar o Bug, por favor preencha devidamente os campos.",
                            "error": 1, "severity": "error"}
        except Exception as e:
            response = {"message": "Error interno: " + str(e), "error": 1, "severity": "error"}
        return JsonResponse(response)


@api_view(['PUT', 'POST', 'GET', 'DELETE'])
def literary_skill(request):
    response = {"message": "Habilidade actualizada com sucesso!", "error": False}

    if request.method == 'PUT':
        lib = LiterarySkills.objects.get(id=int(request.data['id']))
        lib.qualification = string.capwords(request.data['qualification'])
        lib.month = request.data['month']
        lib.year = request.data['year']
        lib.institute = string.capwords(request.data['institute'])
        lib.save()
        return JsonResponse(response)

    if request.method == 'POST':
        data = FormLiterarySkills(request.data)
        if data.is_valid():
            freelancer = Freelancer.objects.get(user=request.user.id)
            freelancer.exp = freelancer.exp + 1
            literarySkill = LiterarySkills.objects.create(freelancer=freelancer, qualification=data['qualification'].value(), month=data['month'].value(), year=data['year'].value(), institute=data['institute'].value())
            literarySkill.save()
            freelancer.save()
        else:
            response = {"message": "Habilidade não foi actualizada, por favor preencha devidamente os campos!", "error": False}
        return JsonResponse(response)

    if request.method == 'GET':
        return HttpResponse(serializers.serialize('json', LiterarySkills.objects.filter(id=int(request.GET['id']))), content_type="application/json")

    if request.method == 'DELETE':
        response = {"error": False}
        LiterarySkills.objects.get(id=int(request.GET['id'])).delete()
        return JsonResponse(response)


@api_view(['PUT', 'POST', 'GET', 'DELETE'])
def payment_method(request):
    response = {"message": "Forma de Recebimento adicionada com sucesso!", "error": False}

    if request.method == 'PUT':
        response = {"message": "Forma de Recebimento actualizada com sucesso!", "error": False}
        gat = FreelaGateway.objects.get(id=int(request.data['id']))
        gat.payment_method = PaymentMethod.objects.get(id=int(request.data['method']))
        gat.account = request.data['reference']
        gat.save()
        return JsonResponse(response)

    if request.method == 'POST':
        freelancer = Freelancer.objects.get(user=request.user.id)
        payment = PaymentMethod.objects.get(id=int(request.data['method']))
        methods = FreelaGateway.objects.filter(freelancer=freelancer)
        methods = methods.filter(payment_method=payment).count()
        if methods == 0:
            freelancer.exp = freelancer.exp + 1
            gat = FreelaGateway.objects.create(freelancer=freelancer, payment_method=payment, account=request.data['reference'])
            gat.save()
            freelancer.save()
        else:
            response = {"message": "Forma de Recebimento já foi adicionada!", "error": True}
        return JsonResponse(response)

    if request.method == 'GET':
        return HttpResponse(serializers.serialize('json', FreelaGateway.objects.filter(id=int(request.GET['id']))), content_type="application/json")

    if request.method == 'DELETE':
        response = {"error": False}
        FreelaGateway.objects.get(id=int(request.GET['id'])).delete()
        return JsonResponse(response)


@api_view(['PUT', 'POST', 'GET'])
def technical_skill(request):
    response = {"message": "Skills actualizados com sucesso!", "severity": "success"}

    if request.method == 'POST':
        try:
            freelancer = Freelancer.objects.get(user=request.user)
            skills = request.data['skills']

            if freelancer.package.max_skill < len(skills):
                response = {"message": "Lamentamos, o seu pacote não permite adicionar mais de {} skills!".format(freelancer.package.max_skill), "severity": "error"}
                return JsonResponse(response)
            
            freelancer.skills.clear()
            freelancer.exp = freelancer.exp + 1
            for skill in skills:
                freelancer.skills.add(Skill.objects.get(id=int(skill)))
            freelancer.save()
        except Exception as e:
            response = {"message": "Erro ao actualizar Skills, por favor tente novamente!", "severity": "error"}
        return JsonResponse(response)

@api_view(['POST', 'GET'])
def send_payment(request):
    package = Package.objects.get(id=int(request.GET['package']))
    message = 'Pagamento efectuado com sucesso.'
    status = 201
    user = request.user
    token = uuid.uuid4()
    PaymentPackage.objects.create(user=request.user, package=package,
                                  payment_method=PaymentMethod.objects.get(id=1), token=token,
                                  expire_at=now() + relativedelta(months=1), mobile=request.GET['phone'],
                                  amount=package.price)
    if not package.price == 0:
        key = 'dsf4utfandhnbwnxtrrs8rlbq97o0x8g'
        pky = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAyrOP7fgXIJgJyp6nP/Vtlu8kW94Qu+gJjfMaTNOSd/mQJChqXiMWsZPH8uOoZGeR/9m7Y8vAU83D96usXUaKoDYiVmxoMBkfmw8DJAtHHt/8LWDdoAS/kpXyZJ5dt19Pv+rTApcjg7AoGczT+yIU7xp4Ku23EqQz70V5Rud+Qgerf6So28Pt3qZ9hxgUA6lgF7OjoYOIAKPqg07pHp2eOp4P6oQW8oXsS+cQkaPVo3nM1f+fctFGQtgLJ0y5VG61ZiWWWFMOjYFkBSbNOyJpQVcMKPcfdDRKq+9r5DFLtFGztPYIAovBm3a1Q6XYDkGYZWtnD8mDJxgEiHWCzog0wZqJtfNREnLf1g2ZOanTDcrEFzsnP2MQwIatV8M6q/fYrh5WejlNm4ujnKUVbnPMYH0wcbXQifSDhg2jcnRLHh9CF9iabkxAzjbYkaG1qa4zG+bCidLCRe0cEQvt0+/lQ40yESvpWF60omTy1dLSd10gl2//0v4IMjLMn9tgxhPp9c+C2Aw7x2Yjx3GquSYhU6IL41lrURwDuCQpg3F30QwIHgy1D8xIfQzno3XywiiUvoq4YfCkN9WiyKz0btD6ZX02RRK6DrXTFefeKjWf0RHREHlfwkhesZ4X168Lxe9iCWjP2d0xUB+lr10835ZUpYYIr4Gon9NTjkoOGwFyS5ECAwEAAQ=='
        skode = '900275'

        api_context = APIContext()
        api_context.api_key = key # 'b5zh48dd1ru963gcjnl4pq0d5ip0cdq0'
        api_context.public_key = pky
        api_context.ssl = True
        api_context.method_type = APIMethodType.POST
        api_context.address = 'api.vm.co.mz' # sandbox
        api_context.port = 18352
        api_context.path = '/ipg/v1x/c2bPayment/singleStage/'

        api_context.add_header('Origin', '*')

        api_context.add_parameter('input_TransactionReference', str(now().year)+'00'+str(user.id))
        api_context.add_parameter('input_CustomerMSISDN', '258' + request.GET['phone'])
        api_context.add_parameter('input_Amount', str(package.price))
        api_context.add_parameter('input_ThirdPartyReference', 'PC000' + str(package.id))
        api_context.add_parameter('input_ServiceProviderCode', skode) # '171717'

        api_request = APIRequest(api_context)
        result = api_request.execute()

        message = 'Pagamento sem sucesso, por favor tente novamente em 5 minutos.'
        status = result.status_code

        if status == 201 or status == 200:
            message = 'Pagamento efectuado com Sucesso!'

        if status == 422:
            message = 'Saldo insuficiente para completar o pagamento, por favor tente novamente!'

    return Response({'status': status, 'token': token, 'message': message})


@api_view(['GET', 'POST'])
def reset_password(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(email=request.GET['email'])
            token = PasswordResetTokenGenerator()
            token = token.make_token(user)

            try:
                userToken = UserToken.objects.get(user=user)
                userToken.token = token
                userToken.save()
            except:
                UserToken.objects.create(user=user, token=token)

            res = send_email('<h5>Olá {},</h5><p>Recebemos um pedido para redefinir sua senha. Se você não fez esse pedido, simplesmente desconsidere essa mensagem e nenhuma outra ação será tomada.!</p><p>Para redefinir sua senha, clique no link: https://www.freela.co.mz/accounts/change_password/?token={}</p><p>O link estará disponível por 10 minutos</p>'.format(
                    user.first_name, token), "Redefinir sua Senha🔓", user.email)

            if res == 500:
                send_email(
                    '<h5>Olá {},</h5><p>Recebemos um pedido para redefinir sua senha. Se você não fez esse pedido, simplesmente desconsidere essa mensagem e nenhuma outra ação será tomada.!</p><p>Para redefinir sua senha, clique no link: https://www.freela.co.mz/accounts/change_password/?token={}</p><p>O link estará disponível por 10 minutos</p>'.format(
                        user.first_name, token), "Redefinir sua Senha🔓", user.email)

            return Response({'error': False, 'message': 'Reset password requested successfully, please see on your MailBox.', 'token': token})
        except Exception as e:
            return Response({'error': True, 'message': 'User with email: ' + request.GET['email'] + ' not found.'})

@api_view(['GET'])
def change_password(request):
    if request.method == 'GET':
        user = request.user
        is_password_valid = check_password(request.GET['old_password'], user.password)
        if is_password_valid:
            user.password = make_password(request.GET['new_password'])
            user.save()
            return Response({'error': is_password_valid, 'message': 'Password Updated Successfully!!'})
        else:
            return Response({'error': False, 'message': 'Invalid Current Password'})


@api_view(['GET'])
def review(request):
    if request.method == 'GET':
        response = {"message": "O seu review foi enviado com sucesso!", "error": False, "severity": "success"}
        try:
            user = request.user
            rate = int(request.GET['rate'])
            freela = int(request.GET['freela'])
            freela = Freelancer.objects.get(id=freela)
            freela.rate = rate
            freela.save()
        except:
            pass
        return Response(response)

@api_view(['POST'])
def save_profile(request):
    response = {"message": "O seu perfil foi actualizado com sucesso!", "error": False, "severity": "success"}

    if request.method == 'POST':
        user = request.user
        data = FormFreelancerProfile(request.data)
        freelancer = Freelancer.objects.get(user=user.id)

        try:
            if data.is_valid():
                name = str(data['name'].value()).split(' ')
                user.first_name = name[0]
                user.last_name = str(data['name'].value()).replace(name[0], "").strip()
                user.save()

                freelancer.job_title = data.data['job_title']
                freelancer.speciality = Category.objects.get(id=int(data.data['speciality']))
                freelancer.salary = data.data['salary']
                freelancer.city = City.objects.get(id=int(data.data['city']))
                freelancer.address = data.data['address']
                freelancer.mobile = data.data['mobile']
                freelancer.overview = data.data['overview']
                freelancer.save()
        except Exception as e:
            response = {"message": "Error interno: " + str(e), "error": True, "severity": "error"}
        return JsonResponse(response)


@api_view(['GET'])
@csrf_exempt
def employer_projects(request):
    return HttpResponse(serializers.serialize('json', Project.objects.filter(employer=Employer.objects.get(user=request.user))), content_type="application/json")