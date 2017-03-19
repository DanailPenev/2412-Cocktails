from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
        url(r'^cocktails/(?P<cocktail_name_slug>[\w\-]+)/$', views.show_cocktail, name='show_cocktail'),
	url(r'^cocktails/upload/$', views.upload_cocktail, name='upload_cocktail'),
	url(r'^about/$', views.about, name='about'),
	url(r'^help/$', views.help, name='help'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^halloffame/$', views.hallOfFame, name='hof'),
        url(r'^recipes/$', views.recipes, name='recipes'),
]
