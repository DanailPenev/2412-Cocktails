from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Cocktail(models.Model):
	name = models.CharField(max_length=128, unique=False, null=False)
	
	def __str__(self):
		return self.name
	
	def __unicode__(self):
		return self.name


class Ingredient(models.Model):
	cocktails = models.ManyToManyField(Cocktail)
	name = models.CharField(max_length=128, unique=True, null=False)
	type = models.CharField(max_length=128, unique=False, null=False)
	
	def __str__(self):
		return self.name
		
	def __unicode__(self):
		return self.type
		
class Instruction(models.Model):
	cocktails = models.ManyToManyField(Cocktail)
	ingredients = models.ManyToManyField(Ingredient)
	type = models.CharField(max_length=128, unique=False, null=False)
	duration = models.IntegerField()
	
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