from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView, CreateView
from btp.forms import ProjectEntryForm, AuthenticationForm, StudentPreferenceEntryForm, AddFacultyForm
from btp.models import  Project, Faculty, Event, ProjectRequests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import password_change, password_change_done
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import date
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

PROJECT_MAX = 3


def is_faculty(user):
	'''
	Returns Whether the requested user is a faculty or not
	'''
	if user:
		return user.groups.filter(name='Faculty').exists()
	return False 

def supervisorParser(supervisors):
	'''
	Returns the cleaned list of all supervisors.
	'''
	faculties = supervisors.split(' ')
	returner = []
	
        for f in faculties:
			username = User.objects.filter(username = f)
			if username :
				fullname = username[0].get_full_name()
				username = username[0].get_username()
				f_dict = { 'fullname':fullname, 'username':username }
				returner.append(f_dict)
		
	return returner				

def summerParser(str_in):
	'''
	Returns a human readable option for summer.
	'''
	SUMMERPARSER = {'01':'This Project demands working during summer, and you\'ll be paid',
			'02':'This Project demands working during summer. There won\'t be any payment',
			'03':'This Project may require working during summer. You\'ll be notified later',
			'04':'This Project doesn\'t require work during summer'
			}
	return SUMMERPARSER[str_in]

def stage_over(stage):
		'''
		returns whether a stage is over or not.
		'''
		event = Event.objects.get(identifier = stage)		
		
		if timezone.now().date() > event.enddate:
			return True
		else:
			return False
			
##########################################################################################################
class HomePageView(FormView):
	'''
	Default Index Page
	'''
	template_name = 'index.html'
	form_class = AuthenticationForm

	def dispatch(self, *args, **kwargs):
	
        	return super(HomePageView, self).dispatch(*args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(HomePageView, self).get_context_data(**kwargs)
		context = { 'title':'BTP@IIITS', 'main_header':'B-Tech Project (BTP) Portal - IIIT - S' ,'nav_list':['faculty','projects','docs'], 'nav_list_len':3 , 'form': AuthenticationForm }
		context['project_requests_exist'] = False
		context['now'] = timezone.now().date
		if not stage_over('STAGE_A'):
			context['stagea'] = True			
			PROJECT_REQUESTS = []
			user = self.request.user	
			projectrequests = ProjectRequests.objects.all()
			for pr in projectrequests:
				if pr.user == user:
					PROJECT_REQUESTS.append(pr)
					context['project_requests_exist'] = True				
		        context['project_requests'] = PROJECT_REQUESTS    
		else:
			context['stagea'] = False
		events = Event.objects.all()
		settings.DATE_FORMAT = '%d %b %Y'
		context['events']=events
		context['is_faculty'] = is_faculty(self.request.user)
		
        	return context
	def form_valid(self, form):
    		redirect_to = settings.LOGIN_REDIRECT_URL
        	auth_login(self.request, form.get_user())
        	if self.request.session.test_cookie_worked():
           		self.request.session.delete_test_cookie()
        	return HttpResponseRedirect(redirect_to)

	def form_invalid(self,form):
		return self.render_to_response(self.get_context_data(form=form))

####################################################################################################
class ProjectEntryView(SuccessMessageMixin, FormView):
	'''
	An Interface for the faculties to enter projects.
	'''

	template_name='project_entry.html'
	form_class=ProjectEntryForm
	success_url = '/btp/projects/'
	
	
	def form_valid(self, form):
		'''
		obtain submitted form fields
		'''
		submitter = str(self.request.user.get_username())
		title = form.cleaned_data['title']
                description = form.cleaned_data['description']
		fileupload = form.cleaned_data['fileupload']
		skillset = form.cleaned_data['skillset']
		summer = form.cleaned_data['summer']
		paid = form.cleaned_data['paid']
		faculty1 = form.cleaned_data['faculty1']
		faculty2 = form.cleaned_data['faculty2']
		faculty3 = form.cleaned_data['faculty3']
		faculty4 = form.cleaned_data['faculty4']
		faculty5 = form.cleaned_data['faculty5']
		
		submitted_faculty_list = []
		
		if faculty1 != 'NA':
			submitted_faculty_list.append( str(faculty1) )
		if faculty2 != 'NA':
			submitted_faculty_list.append( str(faculty2) )
		if faculty3 != 'NA':
			submitted_faculty_list.append( str(faculty3) )
		if faculty4 != 'NA':
			submitted_faculty_list.append( str(faculty4) )
		
		if summer == 'YES' and paid == 'PAID':
			summer = '01'
		elif summer == 'YES' and paid == 'UNPAID':
			summer = '02'
		elif summer == 'MAYBE':
			summer = '03'
		elif summer == 'NO':
			summer = '04'
		
		if submitter in submitted_faculty_list:
			submitter_user = User.objects.get(username=submitter)
			submitter_faculty = Faculty.objects.get(id = submitter_user)
			if submitter_faculty.get_projectcount() < PROJECT_MAX:
				project = Project.objects.create(title=title, supervisor=submitter, description=description, skillset=skillset, summer=summer, postedby=self.request.user, taken=False, fileuploaded=fileupload)
				project.save()
				submitter_faculty.increment_projectcount()
				submitter_faculty.save()
		else:
			project = Project.objects.create(title=title, supervisor='NA', description=description, skillset=skillset, summer=summer, postedby=self.request.user, taken=False, fileuploaded=fileupload)
			project.save()
		
		'''
		Create Project request for other faculties
		'''						 
		
		faculty = 'NA'
		submitted_by = self.request.user
		for supervisor in submitted_faculty_list:
			if supervisor != submitter:
				user_supervisor = User.objects.get(username = supervisor)
				user_supervisor_faculty = Faculty.objects.get(id=user_supervisor)
				if user_supervisor_faculty.get_projectcount() < PROJECT_MAX:
					projectrequest = ProjectRequests.objects.create(user=user_supervisor,submitter=submitted_by, project=project)
					projectrequest.save()	
				
		return super(ProjectEntryView, self).form_valid(form)
	def form_invalid(self,form):
		messages.info(self.request, "Please fill in all the fields in the form")
		return super(ProjectEntryView, self).form_invalid(form)
	def get_context_data(self, **kwargs):
        	context = super(ProjectEntryView, self).get_context_data(**kwargs)
		context = { 'title':'New Project @ IIITS', 'main_header':'B-Tech Project (BTP) Portal - IIIT - S','form':ProjectEntryForm,
			    'sub_header':'Post a new Project'		
		 }
		context['nav_list'] = ['faculty','projects','docs']
		context['nav_list_len'] = 3
        	return context
	@method_decorator(login_required)
	@method_decorator(user_passes_test(is_faculty, login_url = settings.LOGIN_URL))
    	def dispatch(self, *args, **kwargs):
		
        	return super(ProjectEntryView, self).dispatch(*args, **kwargs)
	
#########################################################################################################################################

class ProjectUpdate(UpdateView):
    	model = Project
    	fields = ['title', 'description','skillset', 'fileuploaded']
    	template_name = 'project_update_form.html'
    	success_url = '/projects/'
	def form_valid(self,form):
		title = form.cleaned_data['title']
		description = form.cleaned_data['description']
		skillset = form.cleaned_data['skillset']
		fileuploaded = form.cleaned_data['fileuploaded']
		
		p = Project.objects.get(id=self.kwargs['pk'])
		p.title=title
		p.description=description
		p.skillset=skillset
		p.fileuploaded=fileuploaded
		p.save()
		return super(ProjectUpdate, self).form_valid(form)	
    	def form_invalid(self,form):
		messages.info(self.request, "Please fill in all the fields in the form")	
		return super(ProjectUpdate, self).form_invalid(form)
	def  get_context_data(self, **kwargs):
		context = super(ProjectUpdate, self).get_context_data(**kwargs)
		context['title']='New Project @ IIITS'
		context['main_header']='B-Tech Project (BTP) Portal - IIIT - S'
		context['sub_header']='Post a new Project'		
		context['nav_list'] = ['faculty','projects','docs']
		context['nav_list_len'] = 3
		return context
####################################################################################################
class ProjectPageView(FormView):
	'''
        To Display the Projects entered so far
        '''

	template_name='projects.html'
	form_class = AuthenticationForm
	def dispatch(self, *args, **kwargs):
		if self.request.user.is_active and  self.request.user.last_login == None:
				return password_change(self.request, template_name='changepassword.html', password_change_form=PasswordChangeForm, post_change_redirect='../passwordchanged')
		
	
        	return super(ProjectPageView, self).dispatch(*args, **kwargs)
	def get_context_data(self, **kwargs):
        	context = super(ProjectPageView, self).get_context_data(**kwargs)
		context = { 'title':'Projects | BTP @ IIITS', 'main_header':'B-Tech Project (BTP) Portal - IIIT - S', 'sub_header':' Projects' }
		context['nav_list'] = ['faculty','projects','docs']
		context['nav_list_len'] = 3
		
		FACULTYCALIBERATE = Faculty.objects.all()
		for faculty in FACULTYCALIBERATE:
			faculty.update_projectcount()
			faculty.save()
				
		projects = Project.objects.order_by('title')
		PROJECTS = []
		for project in projects:
			p_dict = {}
			p_dict['id'] = project.id	
			p_dict['title'] = project.title
			if project.description == '':
				p_dict['description'] = 'No description is provided for this project. Please refer to the file uploaded or contact the respective faculty.'
			else:
				p_dict['description'] = project.description
			if project.fileuploaded:
				p_dict['is_fileuploaded'] = True
				p_dict['fileuploaded'] = project.fileuploaded
			else:
				p_dict['is_fileuploaded'] = False
			if project.skillset == '':
				p_dict['skillset'] = 'No expectations / skillset provided for this project.'
			else:
				p_dict['skillset'] = project.skillset
			p_dict['taken'] = project.taken
			supervisors = supervisorParser(project.supervisor)
			p_dict['supervisors'] = supervisors
			p_dict['summer'] = summerParser(project.summer)
			p_dict['editable'] = False
			p_dict['show_project'] = False
			if not stage_over('STAGE_A'):
			   context['stagea'] = True
			   if project.supervisor == 'NA' or project.supervisor == '':
				
				p_dict['dont_show_project']=True
				prs = ProjectRequests.objects.filter(project__id = project.id)
				if not prs:
					project.delete()
					fac = Faculty.objects.get(id = self.request.user.id)
					fac.update_projectcount()	
					fac.save()	
				
			   else:
				p_dict['dont_show_project']=False
			
			else:
			    context['stagea'] = False					
						
			for user in supervisors : 
				if self.request.user.get_username() == user['username']:
					p_dict['editable'] = True
			PROJECTS.append(p_dict)
		if len(PROJECTS) == 0:
			context['projects_flag']= True
			context['projects_flag_message']='There are no projects posted yet.'
		else: 	
			context['projects_flag']=False
			context['projects'] = PROJECTS
		context['form'] = AuthenticationForm
	
		return context
	def form_valid(self, form):
    		redirect_to = settings.LOGIN_REDIRECT_URL
        	auth_login(self.request, form.get_user())
        	if self.request.session.test_cookie_worked():
           		self.request.session.delete_test_cookie()
        	return HttpResponseRedirect(redirect_to)

	def form_invalid(self,form):
		return self.render_to_response(self.get_context_data(form=form))
####################################################################################################
class FacultyPageView(FormView):
	template_name='faculty.html'
	form_class=AuthenticationForm
	def get_context_data(self, **kwargs):
        	context = super(FacultyPageView, self).get_context_data(**kwargs)
		
	
		context = { 'title':'Faculty | BTP @ IIITS', 'main_header':'B-Tech Project (BTP) Portal - IIIT - S', 'sub_header':'Faculty ' }	
		context['nav_list'] = ['faculty','projects','docs']
		context['nav_list_len'] = 3
		faculty = Faculty.objects.order_by('id__first_name') 
		context['faculty'] = faculty
		
		context['form'] = AuthenticationForm
		
		return context

	def form_valid(self, form):
    		redirect_to = settings.LOGIN_REDIRECT_URL
        	auth_login(self.request, form.get_user())
        	if self.request.session.test_cookie_worked():
           		self.request.session.delete_test_cookie()
        	return HttpResponseRedirect(redirect_to)

	def form_invalid(self,form):
		return self.render_to_response(self.get_context_data(form=form))
##################################################################################################################
class DocPageView(FormView):
	'''
	Documentation Page
	'''
	template_name='doc.html'
	form_class = AuthenticationForm
	def get_context_data(self, **kwargs):
        	context = super(DocPageView, self).get_context_data(**kwargs)
		context = { 'title':'Documentation | BTP @ IIITS', 'main_header':'B-Tech Project (BTP) Portal - IIIT - S', 'sub_header':'Documentation' }
		context['nav_list'] = ['faculty','projects','docs']
		context['nav_list_len'] = 3
		context['form'] = AuthenticationForm
		events = Event.objects.all()
		settings.DATE_FORMAT = '%d %b %Y'
		context['events']=events
		
		return context
	def form_valid(self, form):
    		redirect_to = settings.LOGIN_REDIRECT_URL
        	auth_login(self.request, form.get_user())
        	if self.request.session.test_cookie_worked():
           		self.request.session.delete_test_cookie()
        	return HttpResponseRedirect(redirect_to)

	def form_invalid(self,form):
		return self.render_to_response(self.get_context_data(form=form))
#########################################################################################################
class StudentPreferenceEntryView(FormView):
	form_class = StudentPreferenceEntryForm
	template_name = 'preference_entry.html'
	def get_context_data(self, **kwargs):
        	context = super(FacultyPageView, self).get_context_data(**kwargs)
	
	def form_valid():
		student = self.request.user
		preference1 = form.cleaned_data['pref1']
		preference2 = form.cleaned_data['pref2']
		preference3 = form.cleaned_data['pref3']
		partners = form.cleaned_data['partners']
		
	def form_invalid():
		return self.render_to_response(self.get_context_data(form=form))

#############################################################################################################
class AddFacultyView(FormView):
	template_name = 'addfaculty.html'
	form_class = AddFacultyForm
	success_url = '/projects/'
	def form_valid(self,form):
		supervisor = form.cleaned_data['supervisor']
		project = Project.objects.get(id=self.kwargs['pk'])
		user_supervisor = User.objects.get(username = supervisor)
		user_supervisor_faculty = Faculty.objects.get(id=user_supervisor)
		submitted_by = self.request.user
		if user_supervisor_faculty.get_projectcount() < PROJECT_MAX:
				projectrequest = ProjectRequests.objects.create(user=user_supervisor,submitter=submitted_by, project=project)
				projectrequest.save()	
		return super(AddFacultyView, self).form_valid(form)
	def form_invalid(self,form):
		super(AddFacultyView, self).form_invalid(form)
	def  get_context_data(self, **kwargs):
		context = super(AddFacultyView, self).get_context_data(**kwargs)
		context['title']='New Project @ IIITS'
		context['main_header']='B-Tech Project (BTP) Portal - IIIT - S'
		context['sub_header']='Post a new Project'		
		context['nav_list'] = ['faculty','projects','docs']
		context['nav_list_len'] = 3
		return context
		
@login_required
def logout_view(request):
	auth_logout(request)
	return redirect(settings.LOGOUT_URL)

@login_required
def change_password(request):
	return password_change(request, template_name='changepassword.html', password_change_form=PasswordChangeForm, post_change_redirect='../	passwordchanged')
	


def password_changed(request):
	return password_change_done(request, template_name='passwordchanged.html')

def page_not_found(request):
	return render(request,'404.html')

def projectaccept(request, pr_id):
		projectrequest = ProjectRequests.objects.get(id=pr_id)
		project = projectrequest.project
		faculty = Faculty.objects.get(id = request.user.id)
		if project.supervisor != 'NA':
			psupervisor = project.supervisor + ' ' + str(request.user.username)
		else: 
		        psupervisor = str(request.user.username)
		project.update_supervisors(psupervisor)
		project.save()
		faculty.increment_projectcount()
		faculty.save()
		projectrequest.delete()
		return redirect(settings.LOGIN_URL)
def projectreject(request, pr_id):
		projectrequest = ProjectRequests.objects.get(id=pr_id)
		projectrequest.delete()
		
		return redirect(settings.LOGIN_URL)

def projecttaken(request, project_id):
		project = Project.objects.get(id=project_id)
		project.mark_taken()
		project.save()
		return redirect('/projects/')
		
def projectuntaken(request, project_id):
		project = Project.objects.get(id=project_id)
		project.unmark_taken()
		project.save()
		return redirect('/projects/')

def projectdelete(request, project_id):
		project = Project.objects.get(id=project_id)
		faculty = request.user
		supervisors = project.supervisor.split(' ')
		supervisors.remove(str(faculty))
		supervisor_string = ''
		for s in supervisors:
		    	supervisor_string = str(s) + ' '
		if len(supervisors) == 0:	
			supervisor_string='NA'		
		project.supervisor = supervisor_string
		project.save()
		return redirect('/projects/')
		


