from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

# DATABASE MODELS HERE

""" Class Cocktail represents the cocktail entity in the database.
It has the name, picture, rating, author and date attributes.
Slug and author are parsed automatically while the rating default is 0.
It has relationships with user, ingredient, instruction and comment"""
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

"""Class Ingredient represents the ingredient entity in the database.
It has the name, type and quantity attributes, as well as a relationship to Cocktail."""
class Ingredient(models.Model):
	cocktails = models.ManyToManyField(Cocktail)
	name = models.CharField(max_length=128, unique=False, null=False)
	type = models.CharField(max_length=128, unique=False, null=False)
	quantity = models.CharField(max_length=128, unique=False, null=True)
	
	def __str__(self):
		return self.name
		
	def __unicode__(self):
		return self.name

"""Class Instruction represents the instruction entity in the database.
It has the text attribute and a relationship to Cocktail."""		
class Instruction(models.Model):
	cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
	text = models.TextField(unique=False, null=False)

	def __str__(self):
		return self.text

	def __unicode__(self):
		return self.text

"""Class Comment represents the comment entity in the database.
It has the text and date attribtues, a relationship to the user who posted it
and to the cocktail it is posted to."""
class Comment(models.Model):
	text = models.TextField(unique=False, null=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now, blank=True)
	
	def __str__(self):
		return self.text
		
	def __unicode__(self):
		return self.text		

"""Class UserProfile is our extension of the built-in Django User class.
It has the picture, date of birth attributes; a relationship to the user class
and a recursive relationship to itself to allow followers."""		
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