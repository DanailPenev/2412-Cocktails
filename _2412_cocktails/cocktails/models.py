from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

class Cocktail(models.Model):
	name = models.CharField(max_length=128, unique=True, null=False)
	slug = models.SlugField(unique=True)
	picture = models.ImageField(upload_to="cocktail_images", blank=True)
	rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	date = models.DateTimeField(default=timezone.now, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Cocktail, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.name
	
	def __unicode__(self):
		return self.name

class Ingredient(models.Model):
	cocktails = models.ManyToManyField(Cocktail)
	name = models.CharField(max_length=128, unique=False, null=False)
	type = models.CharField(max_length=128, unique=False, null=False)
	quantity = models.CharField(max_length=128, unique=False, null=True)
	
	def __str__(self):
		return self.name
		
	def __unicode__(self):
		return self.name
		
class Instruction(models.Model):
	cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
	text = models.TextField(unique=False, null=False)

	def __str__(self):
		return self.text

	def __unicode__(self):
		return self.text
	
class UserProfile(models.Model):
	#Links UserProfile to a User model instance
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to="profile_pictures", blank=True)	
	dob = models.DateField(auto_now=False, auto_now_add=False)
	follows = models.ManyToManyField('self', related_name='follower', symmetrical=False)
	
	def __str__(self):
		return self.user.username
		
	def __unicode__(self):
		return self.user.username
		
class Comment(models.Model):
	text = models.TextField(unique=False, null=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now, blank=True)
	
	def __str__(self):
		return self.text
		
	def __unicode__(self):
		return self.text