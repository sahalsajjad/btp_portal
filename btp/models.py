from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Student(models.Model):
	id = models.OneToOneField(User, primary_key = True)
	branch = models.CharField(max_length=5) 
	rollno = models.IntegerField()
	def __str__():
		return self.rollno



class Project(models.Model):
	SUMMER_INTERNSHIP_CHOICES = (
    	('01', 'Must work on this project in summer, and you\'ll be paid'),
	('02','Must work on this project in summer, but you\'ll not be paid'),
    	('03', 'May have to work in summer, can\'t say at this time'),
    	('04', 'You dont have to work during summer'))
	

	title = models.CharField(max_length=150)
	description = models.TextField(default='NA')
	supervisor = models.TextField(default='NA')
	skillset=models.TextField(default='NA')
	summer = models.CharField(max_length=5, choices=SUMMER_INTERNSHIP_CHOICES, default='04')
	postedby = models.ForeignKey(User, related_name='project_postedby')
	taken = models.BooleanField(default=False)
	isfileuploaded = models.BooleanField(default=False)
	fileuploaded = models.FileField(null=True,blank=True,upload_to='')

	def __str__(self):
		
		return self.title
	
	def get_supervisors(self):
		SUPERVISORS = self.supervisor.split(' ')
		
		return SUPERVISORS
	def update_supervisors(self, supervisors):
		self.supervisor = supervisors
		return  True
	def mark_taken(self):
		self.taken = True
	def unmark_taken(self):
		self.taken = False
	
	
class Faculty(models.Model):
	id = models.OneToOneField(User, primary_key = True)
	institute=models.CharField(max_length=200)
	projectcount = models.IntegerField(default=0,editable=True)
	def __str__(self):
		return str(self.id)
	
	def fullname(self):
		return str(User.objects.get(username = self.id).get_full_name())
		
	def get_projectcount(self):
		return self.projectcount
	def increment_projectcount(self):
		self.projectcount+=1
	def decrement_projectcount(self):
		self.projectcount-=1

		
	
	def get_projects(self):
		projects = Project.objects.all()
		PLIST = []
		for p in projects:
			checklist = p.get_supervisors()
			if str(self.id.get_username()) in checklist:
				PLIST.append(p)
		return PLIST
	def update_projectcount(self):
		P = self.get_projects()
		self.projectcount = len(P)
	def no_projects(self):
		return (self.projectcount == 0)
			
class ProjectRequests(models.Model):
	user = models.ForeignKey(User, related_name='request_to')
	submitter = models.ForeignKey(User, related_name='request_by')
	project = models.ForeignKey(Project)
	
class Event(models.Model):
	identifier = models.CharField(max_length=20)
	event = models.CharField(max_length=250)
	description = models.TextField()
	startdate= models.DateField() 
	enddate= models.DateField()
	def __str__(self):
		return self.event
	def days_to_start(self):
		self.startdate - timezone.now().date 
	def days_to_end(self):
		self.enddate - timezone.now().date
	
		

class Preference(models.Model):
	student = models.OneToOneField(User)
	pref1 = models.ForeignKey(Project, related_name='project_preference_1')
	pref2 = models.ForeignKey(Project, related_name='project_preference_2')
	pref3 = models.ForeignKey(Project, related_name='project_preference_3')
	partners = models.TextField(default='NA')
		
