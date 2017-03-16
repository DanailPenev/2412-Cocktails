from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^cocktail/(?P<cocktail_name_slug>[\w\-]+)/$', views.show_cocktail, name='show_cocktail'),
	url(r'^cocktail/upload/$', views.upload_cocktail, name='upload_cocktail'),
	url(r'^about/$', views.about, name='about'),
	url(r'^help/$', views.help, name='help'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
]