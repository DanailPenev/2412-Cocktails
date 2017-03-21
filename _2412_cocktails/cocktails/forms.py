from django import forms
from cocktails.models import *
from django.forms import formset_factory

years = range(1900, 1999)
BIRTH_YEAR_CHOICES = []
for i in years:
	BIRTH_YEAR_CHOICES.append(str(i))

class CocktailForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter cocktail name.")

	class Meta:
		model = Cocktail
		fields = ('name', 'picture')

class IngredientForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter ingredient.")
	quantity = forms.CharField(max_length=128, help_text="Enter quantity and quantifier(e.g. table spoons, ml, etc.")
	type = forms.CharField(max_length=128, help_text="Enter type, i.e. alcoholic, non-alcoholic, fruit, etc.")

	class Meta:
		model = Ingredient
		exclude = ('cocktails',)
		
IngredientFormSet = formset_factory(IngredientForm, extra=0)

class InstructionForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea, help_text="Enter the instruction.")

	class Meta:
		model = Instruction
		fields = ('text',)

InstructionFormSet = formset_factory(InstructionForm, extra=0)
		
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form'}))

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class UserProfileForm(forms.ModelForm):
	dob = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES, attrs={'class': 'form'}))
	picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form'}))

	class Meta:
		model = UserProfile
		fields = ('dob', 'picture')