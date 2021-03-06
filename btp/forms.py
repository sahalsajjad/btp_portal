from django.forms import ModelForm, TextInput, Textarea, EmailInput, PasswordInput, Select, ChoiceField, CharField, EmailField, Form, MultipleChoiceField, FileField, ClearableFileInput
from btp.models import Project, Faculty, Student
from django.contrib import auth
from django.contrib.auth.models import User

FACULTYLIST = list()
temp_tup = tuple(['NA','-----------'])
FACULTYLIST.append(temp_tup)
#FACULTIES = Faculty.objects.all()
FACULTIES = Faculty.objects.order_by('id__first_name')

for faculty in FACULTIES:
	fid = faculty.id
	fuser = str(fid.get_username())
	fname = str(fid.get_full_name())
	temp_tup = list()
	temp_tup.append(fuser)
	temp_tup.append(fname)
	temp_tup = tuple(temp_tup)
	FACULTYLIST.append(temp_tup)

FACULTYLIST = tuple(FACULTYLIST)

STUDENTLIST = list()
temp_tup = tuple(['NA','-----------'])
STUDENTLIST.append(temp_tup)
STUDENTS = Student.objects.all()
for student in STUDENTS:
	sid = student.id
	suser = str(sid.get_username())
	sname = str(sid.get_full_name())					

PROJECTLIST = list()
temp_tup = tuple(['NA','-----------'])
PROJECTLIST.append(temp_tup)
PROJECTS = Project.objects.all()
for project in PROJECTS:
	pid = project.id
	ptitle = project.title

SUMMER_INTERNSHIP_CHOICES = (
    	('YES', 'Yes - Must work on this project'),
    	('MAYBE', 'May be/ May not be - negotiable'),
    	('NO', 'No'))
SUMMER_INTERNSHIP_PAYMENT_CHOICES = (
	('PAID', 'Paid'),
    	('UNPAID', 'Unpaid'))

class AuthenticationForm(auth.forms.AuthenticationForm):
	'''
	Login Form which inherits from Django auth model
	'''
	username = CharField(label='',required=True, widget=TextInput(attrs={'class':'form-control','placeholder':'Enter your email address'}))
	password = CharField( label='',widget=PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}), max_length=50, required=True, )
	widgets = {
            	'password': PasswordInput(),
       	}

class ProjectEntryForm(Form):
	'''
	A form for the faculties to Enter the projects offered
	'''
	title = CharField(widget=TextInput(attrs={'id':'project-form-title','class':'form-control'}), label='Domain/Title of the Project')
	description = CharField(required=False,widget=Textarea(attrs={'id':'project-form-description','class':'form-control','rows':5}),label='Brief description about the project')
	fileupload = FileField(required=False, widget=ClearableFileInput(attrs={'id':'project-form-upload'}), label='Upload a file (optional)')
	faculty1 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	faculty2 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	faculty3 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	faculty4 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	faculty5 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	skillset=CharField(required=False,widget=Textarea(attrs={'id':'project-form-skillset','class':'form-control','rows':5}),label='Expectations/Skillset for this project')
	
	summer = ChoiceField( choices=SUMMER_INTERNSHIP_CHOICES, initial='NO', widget=Select(attrs={'id':'project-form-summer','class':'form-control'}), label='Should the student work on this project during the summer?')

	paid = ChoiceField( choices=SUMMER_INTERNSHIP_PAYMENT_CHOICES, widget=Select(attrs={'id':'project-form-paid','class':'form-control'}),label='Will the summer work be paid?')

class StudentPreferenceEntryForm(Form):
	
	pref1 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	pref2 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	pref3 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	partner1 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	partner2 = ChoiceField(choices=FACULTYLIST, widget=Select(attrs={'id':'project-form-faculty','class':'form-control'}), label='Faculty/Supervisor name')
	
class EditProjectForm(Form):
	'''
	A form for the faculties to Enter the projects offered
	'''
	title = CharField(widget=TextInput(attrs={'id':'project-form-title','class':'form-control'}), label='Domain/Title of the Project')
	description = CharField(required=False,widget=Textarea(attrs={'id':'project-form-description','class':'form-control','rows':5}),label='Brief description about the project')
	fileupload = FileField(required=False, widget=ClearableFileInput(attrs={'id':'project-form-upload'}), label='Upload a file (optional)')
	
	skillset=CharField(required=False,widget=Textarea(attrs={'id':'project-form-skillset','class':'form-control','rows':5}),label='Expectations/Skillset for this project')
	
	summer = ChoiceField( choices=SUMMER_INTERNSHIP_CHOICES, initial='NO', widget=Select(attrs={'id':'project-form-summer','class':'form-control'}), label='Should the student work on this project during the summer?')

	paid = ChoiceField( choices=SUMMER_INTERNSHIP_PAYMENT_CHOICES, widget=Select(attrs={'id':'project-form-paid','class':'form-control'}),label='Will the summer work be paid?')

class AddFacultyForm(Form):
	supervisor = ChoiceField(choices = FACULTYLIST , widget=Select(attrs={'id':'add-faculty','class':'form-control'}), label='Faculty/Supervisor name')


	
		


