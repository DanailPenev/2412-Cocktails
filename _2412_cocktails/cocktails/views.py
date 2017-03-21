from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cocktails.models import *
from cocktails.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	context_dict = {}
	cocktails = Cocktail.objects.order_by('-rating')[:3]
	context_dict['cocktails'] = cocktails
	return render(request, 'cocktails/index.html', context_dict)

def about(request):
	return render(request, 'cocktails/about.html', {})
	
def help(request):
	return render(request, 'cocktails/help.html', {})
	
def hallOfFame(request):
	context_dict = {}
	cocktails = Cocktail.objects.order_by('-rating')[:5]
	context_dict['cocktails'] = cocktails
	return render(request, 'cocktails/hof.html', context_dict)

def register(request):
	# was the registration successful
	# initially false
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			
			profile.save()
			
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			print(user_form.errors, profile_form.errors)
			
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	
	return render(request, 'cocktails/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details")
			
	else:
		return render(request, 'cocktails/login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

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

@login_required	
def upload_cocktail(request):
	# successful upload?
	uploaded = False
	
	if request.method == 'POST':
		cocktail_form = CocktailForm(data=request.POST)
		ingredientSet = IngredientFormSet(data=request.POST)
		for ingredient in ingredientSet.forms:
			print ingredient
		instructionSet = InstructionFormSet(data=request.POST)
		for instruction in instructionSet:
			print instruction
			
	else:
		cocktail_form = CocktailForm()
		ingredientSet = IngredientFormSet()
		instructionSet = InstructionFormSet()
		
	context_dict = {}
	context_dict['cocktail_form'] = cocktail_form
	context_dict['ingredientSet'] = ingredientSet
	context_dict['instructionSet'] = instructionSet
	return render(request, 'cocktails/upload_cocktail.html', context_dict)
		
def cocktails(request):
    return render(request, 'cocktails/cocktails.html', {})

def profile(request):
	return render(request, 'cocktails/profile.html', {})
