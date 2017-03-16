from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Cocktail(models.Model):
	name = models.CharField(max_length=128, unique=True, null=False)
	slug = models.SlugField(unique=True)
	rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)

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
	cocktail = models.ForeignKey(Cocktail)
	text = models.TextField(unique=False, null=False)

	def __str__(self):
		return self.text

	def __unicode__(self):
		return self.text
	
class UserProfile(models.Model):
	#Links UserProfile to a User model instance
	user = models.OneToOneField(User)
	followee = models.ForeignKey('self', null=True)
	
	dob = models.DateField(auto_now=False, auto_now_add=False)
	
	def save(self, checkFollowee=True):
		super(UserProfile, self).save()
		if self.partner and checkFollowee:
			self.followee.followee = self
			self.followee.save(checkPartner=False)