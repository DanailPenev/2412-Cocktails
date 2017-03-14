from django.shortcuts import render
from django.http import HttpResponse
from cocktails.models import *

# Create your views here.
def index(request):
	return HttpResponse("Hello, world. You're at the index, babyy.")

def show_cocktail(request, cocktail_name_slug):
	context_dict = {}

	try:
		cocktail = Cocktail.objects.get(slug=cocktail_name_slug)

		ingredients = Ingredient.objects.filter(cocktail=cocktail)
		instructions = Instruction.objects.filter(cocktail=cocktail)

		context_dict['ingredients'] = ingredients
		context_dict['instructions'] = instructions
		context_dict['cocktail'] = cocktail

	except Cocktail.DoesNotExist:
		context_dict['ingredients'] = None
		context_dict['instructions'] = None
		context_dict['cocktail'] = None

	return render(request, 'cocktails/cocktail.html', context_dict)	