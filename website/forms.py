from django import forms

class FormFreelancerSearch(forms.Form):
    query = forms.CharField(label='query', max_length=100, required=False)
    speciality = forms.CharField(label='speciality', required=False)
    address = forms.CharField(label='address', max_length=100, required=False)
    skills = forms.MultipleChoiceField(widget=forms.SelectMultiple)

class FormProjectSearch(forms.Form):
    query = forms.CharField(label='query', max_length=100, required=False)
    speciality = forms.CharField(label='speciality', required=False)
    budget = forms.CharField(label='budget', required=False)
    experience = forms.CharField(label='experience', required=False)

class FormUploadAlbum(forms.Form):
    hashtag = forms.CharField(label='hashtag', max_length=250)
    picture = forms.CharField(label='picture', required=True)

class FormAlbum(forms.Form):
    title = forms.CharField(label='title', max_length=250, required=True)
    category = forms.IntegerField(label='category', required=True)

class FormLogin(forms.Form):
    email = forms.EmailField(label='email', required=True)
    password = forms.CharField(label='password', required=True)

class FormUserRegister(forms.Form):
    name = forms.CharField(label='name', max_length=250, required=True)
    email = forms.EmailField(label='email', max_length=150, required=True)
    password = forms.CharField(label='password', max_length=250, required=True)

class FormFreelancerProfile(forms.Form):
    name = forms.CharField(label='name', max_length=250)
    job_title = forms.CharField(label='job_title', max_length=250)
    speciality = forms.CharField(label='speciality', max_length=250)
    salary = forms.CharField(label='salary', max_length=250)
    city = forms.CharField(label='city', max_length=250, required=False)
    address = forms.CharField(label='address', max_length=250, required=False)
    mobile = forms.CharField(label='mobile', max_length=250, required=False)
    overview = forms.CharField(label='overview', required=False)

class FormEmployerProfile(forms.Form):
    name = forms.CharField(label='name', max_length=250)
    speciality = forms.CharField(label='speciality', max_length=250)
    overview = forms.CharField(label='overview', required=False)

class FormEmployerProject(forms.Form):
    title = forms.CharField(label='title', max_length=250)
    category = forms.IntegerField(label='category')
    experience = forms.IntegerField(label='experience')
    budget = forms.IntegerField(label='budget')
    deadline = forms.IntegerField(label='deadline')
    overview = forms.CharField(label='overview', required=False)

class FormProposalProject(forms.Form):
    project = forms.IntegerField(label='project')
    budget = forms.CharField(label='budget')
    deadline = forms.IntegerField(label='deadline')
    description = forms.CharField(label='description')


class FormProjectInvite(forms.Form):
    freelancer = forms.CharField(label='freelancer', required=True)
    category = forms.CharField(label='category', required=True)
    budget = forms.CharField(label='budget', required=True)
    exclusive = forms.BooleanField(label='exclusive', required=False)
    title = forms.CharField(label='title', required=True)
    description = forms.CharField(label='description', required=True)


class FormLiterarySkills(forms.Form):
    qualification = forms.CharField(label='qualification', required=True)
    month = forms.IntegerField(label='month', required=True)
    year = forms.IntegerField(label='year', required=True)
    institute = forms.CharField(label='institute', required=True)

class FormSkills(forms.Form):
    skills = forms.MultipleChoiceField(widget=forms.SelectMultiple)


class FormBugReport(forms.Form):
    title = forms.CharField(label='title', required=True)
    type = forms.IntegerField(label='type', required=True)
    url = forms.CharField(label='url', required=True)
    description = forms.CharField(label='description', required=True)