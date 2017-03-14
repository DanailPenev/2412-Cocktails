from django import forms
from cocktails.models import *

class CocktailForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter cocktail name.")

	class Meta:
		model = Cocktail
		fields = ('name',)

class IngredientForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter ingredient.")
	quantity = forms.CharField(max_length=128, help_text="Enter quantity and quantifier(e.g. table spoons, ml, etc.")
	type = forms.CharField(max_length=128, help_text="Enter type, i.e. alcoholic, non-alcoholic, fruit, etc.")

	class Meta:
		model = Ingredient
		exclude = ('cocktails',)

class InstructionForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea, help_text="Enter the instruction.")

	class Meta:
		model = Instruction
		fields = ('text',)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('dob',)