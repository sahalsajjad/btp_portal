from django.contrib import admin
from btp.models import Student, Faculty,  Project, Event, ProjectRequests

admin.site.register(Project)
admin.site.register(ProjectRequests)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Event)
