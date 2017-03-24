from django import forms
from cocktails.models import *
from django.forms import formset_factory

# FORMS THAT WILL BE DISPLAYED IN THE TEMPLATES TO GET USER INPUT

# variables we will use for the date of birth form
years = range(1900, 1999)
BIRTH_YEAR_CHOICES = []
for i in years:
	BIRTH_YEAR_CHOICES.append(str(i))

	
# CocktailForm uses the Cocktail model to create new objects
class CocktailForm(forms.ModelForm):
	name = forms.CharField(max_length=128)
	picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form'}))

	class Meta:
		model = Cocktail
		fields = ('name', 'picture')

# IngredientForm uses the Ingredient model to create new objects
class IngredientForm(forms.ModelForm):
	name = forms.CharField(required=False, max_length=128)
	quantity = forms.CharField(required=False, max_length=128)
	type = forms.CharField(required=False, max_length=128)

	class Meta:
		model = Ingredient
		exclude = ('cocktails',)

# InstructionForm uses the Instruction model to create new objects		
class InstructionForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}))

	class Meta:
		model = Instruction
		fields = ('text',)

# We create formsets for Ingredient and Instruction in order to have more than one form displayed
IngredientFormSet = formset_factory(IngredientForm)
InstructionFormSet = formset_factory(InstructionForm)

# UserForm uses the built-in User model	to create new objects
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form'}))

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

# UserProfileForm uses the UserProfile model to create new objects
class UserProfileForm(forms.ModelForm):
	dob = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES, attrs={'class': 'form'}))
	picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form'}))

	class Meta:
		model = UserProfile
		fields = ('dob', 'picture')