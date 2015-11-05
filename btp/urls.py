from django.conf.urls import url
from btp.views import ProjectEntryView, HomePageView, ProjectPageView, FacultyPageView, DocPageView, logout_view, change_password, password_changed, page_not_found, projectaccept, projectreject, projectdelete, ProjectUpdate, AddFacultyView, projecttaken, projectuntaken
from django.conf import settings
urlpatterns = [
	url(r'^$', HomePageView.as_view(), name='homepage'),
	url(r'project/new/$', ProjectEntryView.as_view(), name='projectentry'),
	url(r'docs/$', DocPageView.as_view(), name='docs'),
	url(r'faculty/$', FacultyPageView.as_view(), name='faculty'),
	url(r'projects/$', ProjectPageView.as_view(), name='projects'),
	url(r'signout/$', logout_view, name='signout'),
	url(r'changepassword/$', change_password ,name='changepassword'),
	url(r'passwordchanged/$', password_changed, name='passwordchanged'),
	url(r'projectaccept/([0-9]+)/', projectaccept, name='project-accept'),
	url(r'projectreject/([0-9]+)/', projectreject, name='project-reject'),
	url(r'project/edit/(?P<pk>\d+)$',ProjectUpdate.as_view(), name='project-update'),
	url(r'project/add/(?P<pk>\d+)$',AddFacultyView.as_view(), name='add-faculty'),
	url(r'project/taken/([0-9]+)/', projecttaken, name='project-taken'),
	url(r'project/untaken/([0-9]+)/', projectuntaken, name='project-untaken'),
	url(r'project/delete/([0-9]+)/',projectdelete, name='project-delete'),	
]
if settings.SERVE_MEDIA:
    urlpatterns += (
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, }),
)
