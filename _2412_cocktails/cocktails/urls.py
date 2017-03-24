from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^help/$', views.help, name='help'),
	
	# user functionality urls
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^users/(?P<user_name>[\w\-]+)/$', views.get_user, name='get_user'),
	url(r'^users/(?P<user_name>[\w\-]+)/follow/$', views.follow_user, name='follow_user'),
	url(r'^users/(?P<user_name>[\w\-]+)/unfollow/$', views.unfollow_user, name='unfollow_user'),
	url(r'^change_password/$', views.change_password, name='change_password'),
	url(r'^delete_user/$', views.delete_user, name='delete_user'),
	
	# cocktail urls
	url(r'^cocktails/upload/$', views.upload_cocktail, name='upload_cocktail'),
	url(r'^cocktails/category/(?P<category>[\w\-]+)/$', views.show_cocktail_category, name='show_cocktail_category'),
    url(r'^cocktails/(?P<cocktail_name_slug>[\w\-]+)/$', views.show_cocktail, name='show_cocktail'),
	url(r'^cocktails/(?P<cocktail_name_slug>[\w\-]+)/edit/$', views.edit_cocktail, name='edit_cocktail'),
	url(r'^cocktails/(?P<cocktail_name_slug>[\w\-]+)/delete/$', views.delete_cocktail, name='delete_cocktail'),
	url(r'^cocktails/(?P<cocktail_name_slug>[\w\-]+)/rate/$', views.rate_cocktail, name='rate'),
	url(r'^cocktails/(?P<cocktail_name_slug>[\w\-]+)/comment/$', views.add_comment, name='comment'),
	url(r'^cocktails/$', views.cocktails, name='cocktails'),
	url(r'^halloffame/$', views.hallOfFame, name='hof'),
]