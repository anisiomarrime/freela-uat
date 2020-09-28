from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class City(models.Model):
    description = models.CharField(max_length=150, unique=True)
    objects = models.Manager()

class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)
    objects = models.Manager()

class PackageFeature(models.Model):
    name = models.CharField(max_length=150, unique=True)
    objects = models.Manager()

class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    features = models.ManyToManyField(PackageFeature, related_name="package_features")
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    max_category = models.IntegerField()
    max_follow = models.IntegerField()
    max_skill = models.IntegerField()
    max_project = models.IntegerField()
    is_customer_chat = models.BooleanField()
    is_premium = models.BooleanField()
    is_notification = models.BooleanField()
    objects = models.Manager()

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    objects = models.Manager()

class FreelancerStats(models.Model):
    projects_end = models.IntegerField(default=0)
    projects_con = models.IntegerField(default=0)
    proposals_sent = models.IntegerField(default=0)
    customer_reviews = models.IntegerField(default=0)
    violations = models.IntegerField(default=0)
    certifications = models.IntegerField(default=0)
    objects = models.Manager()

class PaymentMethod(models.Model):
    name = models.CharField(max_length=250, unique=True)
    status = models.IntegerField(default=1)
    objects = models.Manager()

class Freelancer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    slug = models.SlugField(max_length=150)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=1)
    speciality = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    skills = models.ManyToManyField(Skill, related_name="freelancer_skills")
    stats = models.ForeignKey(FreelancerStats, on_delete=models.CASCADE, default=1)
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    exp = models.IntegerField(default=0)
    photo = models.TextField(default='avatar.png')
    job_title = models.CharField(max_length=200, default='Freelancer no Freela')
    salary = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=150, default='Maputo, Moçambique')
    mobile = models.CharField(max_length=20, default='+258')
    overview = models.TextField(default='Ola! estou no Freela...')
    status = models.BooleanField(default=1)
    is_main = models.BooleanField(default=0)
    objects = models.Manager()


class PaymentPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, editable=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=1)
    token = models.CharField(max_length=250, editable=False)
    mobile = models.CharField(max_length=14, editable=False)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=now)
    expire_at = models.DateTimeField(default=now)
    objects = models.Manager()


class FreelaGateway(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, editable=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, editable=False)
    account = models.CharField(max_length=150)
    objects = models.Manager()


class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(max_length=150)
    speciality = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200, default='')
    photo = models.TextField(default='logo.png')
    overview = models.TextField(default='')
    mobile = models.CharField(max_length=20, default='+258')
    status = models.BooleanField(default=1)
    is_main = models.BooleanField(default=0)
    payment_verified = models.BooleanField(default=0)
    objects = models.Manager()

class Status(models.Model):
    name = models.CharField(max_length=150, unique=True)
    objects = models.Manager()


class Newsletter(models.Model):
    email = models.CharField(max_length=250, unique=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=now)
    objects = models.Manager()


class Budget(models.Model):
    min_value = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    max_value = models.DecimalField(decimal_places=2, max_digits=10, default=1.00)
    objects = models.Manager()

class ExperienceLevel(models.Model):
    name = models.CharField(max_length=150, unique=True)
    objects = models.Manager()

class Chat(models.Model):
    token = models.CharField(max_length=255, unique=True, editable=False)
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first_user")
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_user")
    created_at = models.DateTimeField(default=now)
    objects = models.Manager()

class Project(models.Model):
    title = models.CharField(max_length=200, default='')
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, editable=False)
    skills = models.ManyToManyField(Skill, related_name="project_skills")
    slug = models.SlugField(max_length=150)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    experience = models.ForeignKey(ExperienceLevel, default=1, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, default=1, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, default=4, on_delete=models.CASCADE)
    deadline = models.IntegerField(default=10)
    overview = models.TextField(default='')
    close_at = models.DateTimeField(default=datetime.now, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    is_exclusive = models.BooleanField(default=0)
    objects = models.Manager()

class Proposal(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, editable=False)
    budget = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    deadline = models.IntegerField(default=10)
    description = models.TextField(default='')
    status = models.ForeignKey(Status, default=3, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    objects = models.Manager()

class ProjectInvite(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, editable=False)
    budget = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    status = models.ForeignKey(Status, default=3, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    objects = models.Manager()

class LiterarySkills(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, editable=False)
    qualification = models.CharField(max_length=250)
    month = models.IntegerField(default=1)
    year = models.IntegerField(default=2020)
    institute = models.CharField(max_length=250)
    objects = models.Manager()

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    token = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=True)
    objects = models.Manager()

class FreelaReviews(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, editable=False)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, editable=False)
    review = models.TextField(default='')
    rate = models.IntegerField(default=0)
    objects = models.Manager()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name="user")
    target = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name="target")
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    is_opened = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=now)
    objects = models.Manager()


class BugType(models.Model):
    name = models.CharField(max_length=150, unique=True)
    reward = models.DecimalField(max_digits=5, decimal_places=2)
    objects = models.Manager()

class BugReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    bug_type = models.ForeignKey(BugType, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=250)
    description = models.CharField(max_length=450)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    is_reward = models.BooleanField(default=0)
    objects = models.Manager()

class Reward(models.Model):
    bug_report = models.ForeignKey(BugReport, on_delete=models.CASCADE, editable=False)
    reward_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    reward = models.DecimalField(max_digits=2, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    objects = models.Manager()
