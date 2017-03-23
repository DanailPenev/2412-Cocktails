from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cocktails.models import *
from cocktails.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

@login_required	
def hallOfFame(request):
	context_dict = {}
	cocktails = Cocktail.objects.order_by('-rating')[:6]
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

@login_required	
def upload_cocktail(request):
	# successful upload?
	uploaded = False
	
	if request.method == 'POST':
		cocktail_form = CocktailForm(data=request.POST)
		ingredientSet = IngredientFormSet(data=request.POST, prefix="fs1")
		instructionSet = InstructionFormSet(data=request.POST, prefix="fs2")
		if cocktail_form.is_valid() and ingredientSet.is_valid() and instructionSet.is_valid():
			cocktail = cocktail_form.save(commit=False)
			if 'picture' in request.FILES:
				cocktail.picture = request.FILES['picture']
			cocktail.author = request.user
			cocktail.save()
			ingredientSet = ingredientSet.cleaned_data
			for i in ingredientSet:
				temp = Ingredient.objects.get_or_create(quantity=i['quantity'], name=i['name'])
				ingredient = temp[0]
				if (temp[1]):
					ingredient.type = i['type']				
				ingredient.cocktails.add(cocktail)
				ingredient.save()
			instructionSet = instructionSet.cleaned_data
			for i in instructionSet:
				instruction = Instruction.objects.get_or_create(cocktail=cocktail, text=i['text'])[0]
				instruction.save()
		return HttpResponseRedirect(reverse('index'))
			
	else:
		cocktail_form = CocktailForm()
		ingredientSet = IngredientFormSet(prefix="fs1")
		instructionSet = InstructionFormSet(prefix="fs2")
		
	context_dict = {}
	context_dict['cocktail_form'] = cocktail_form
	context_dict['ingredientSet'] = ingredientSet
	context_dict['instructionSet'] = instructionSet
	return render(request, 'cocktails/upload_cocktail.html', context_dict)	
	
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
			return HttpResponse("Invalid login details")
			
	else:
		par = request.GET.get('next', '')
		redirected = False
		if par != '':
			redirected = True
		return render(request, 'cocktails/login.html', {'redirected': redirected})

@login_required
def change_password(request):
	context_dict = {}
	if request.method == 'POST':
		successful = False

		password = request.POST.get('old_password')
		new_pass_1 = request.POST.get('new_password')
		new_pass_2 = request.POST.get('new_password_again')
		u = request.user
		auth = authenticate(username=u.username, password=password)
		if new_pass_1==new_pass_2 and auth:
			u.set_password(new_pass_2)
			u.save()
			successful = True
			context_dict['successful'] = successful
			return render(request, 'cocktails/change_password.html', context_dict)
	return render(request, 'cocktails/change_password.html', context_dict)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def delete_user(request):
	u = request.user
	logout(request)
	User.objects.filter(username=u.username).delete()
	return HttpResponseRedirect(reverse('index'))

@login_required
def show_cocktail(request, cocktail_name_slug):
	context_dict = {}

	try:
		cocktail = Cocktail.objects.get(slug=cocktail_name_slug)
		ingredients = cocktail.ingredient_set.all()
		instructions = cocktail.instruction_set.all()
		owner = request.user==cocktail.author

		context_dict['ingredients'] = ingredients
		context_dict['instructions'] = instructions
		context_dict['cocktail'] = cocktail
		context_dict['owner'] = owner

	except Cocktail.DoesNotExist:
		context_dict['ingredients'] = None
		context_dict['instructions'] = None
		context_dict['cocktail'] = None
		context_dict['owner'] = False

	return render(request, 'cocktails/show_cocktail.html', context_dict)	

@login_required
def show_cocktail_category(request, category):
	context_dict = {}
	cocktails = []
	for cocktail in Cocktail.objects.all():
		for ingredient in cocktail.ingredient_set.all():
			if ingredient.name.lower()==category.lower():
				cocktails.append(cocktail)
				break
	context_dict['cocktails'] = cocktails
	return render(request, 'cocktails/show_cocktail_category.html', context_dict)
	
@login_required
def rate_cocktail(request, cocktail_name_slug):
	context_dict = {}
	cocktail = Cocktail.objects.get(slug=cocktail_name_slug)
	rate = int(request.POST.get('rating'))
	voted = True
	cocktail.rating = (cocktail.rating + rate)/2
	cocktail.save()
	ingredients = cocktail.ingredient_set.all()
	instructions = cocktail.instruction_set.all()
	owner = request.user==cocktail.author
	context_dict['ingredients'] = ingredients
	context_dict['instructions'] = instructions
	context_dict['cocktail'] = cocktail
	context_dict['owner'] = owner
	context_dict['voted'] = voted
	return render(request, 'cocktails/show_cocktail.html', context_dict)

@login_required
def cocktails(request):
    cocktails = Cocktail.objects.all().order_by('-date')
    #Paginator
    page = request.GET.get('page', 1)

    paginator = Paginator(cocktails, 6)

    try:
    	cocktail_recipes = paginator.page(page)

    except PageNotAnInteger:
    	cocktail_recipes = paginator.page(1)

    except EmptyPage:
    	cocktail_recipes = paginator.page(paginator.num_pages)

    return render(request, 'cocktails/cocktails.html', { 'cocktails': cocktail_recipes})

@login_required	
def get_user(request, user_name):
	context_dict = {}
	user = User.objects.get(username=user_name)
	cocktails = Cocktail.objects.filter(author=user)
	# Paginator
	page = request.GET.get('page', 1)

        paginator = Paginator(cocktails, 6)

        try:
                cocktail_recipes = paginator.page(page)

        except PageNotAnInteger:
                cocktail_recipes = paginator.page(1)

        except EmptyPage:
                cocktail_recipes = paginator.page(paginator.num_pages)

	owner = user==request.user
	uploads = len(cocktail_recipes)
	following = False
	if not owner and user.userprofile in request.user.userprofile.follows.all():
		following = True
	follows = len(user.userprofile.follows.all())
	followers = user.userprofile.follower.all()
	context_dict['user'] = user
	context_dict['cocktails'] = cocktail_recipes
	context_dict['owner'] = owner
	context_dict['following'] = following
	context_dict['uploads'] = uploads
	context_dict['follows'] = follows
	context_dict['followers'] = followers
	return render(request, 'cocktails/profile.html', context_dict)

@login_required
def follow_user(request, user_name):
	context_dict = {}
	user = User.objects.get(username=user_name)
	follower = request.user
	follower.userprofile.follows.add(user.userprofile)
	return HttpResponseRedirect(reverse('get_user', kwargs={'user_name': user.username}))
	
@login_required
def unfollow_user(request, user_name):
	context_dict = {}
	user = User.objects.get(username=user_name)
	follower = request.user
	following = True
	if user.userprofile in request.user.userprofile.follows.all():
		follower.userprofile.follows.remove(user.userprofile)
		following = False
	return HttpResponseRedirect(reverse('get_user', kwargs={'user_name': user.username}))

@login_required
def profile(request):
	context_dict = {}
	user = request.user
	return HttpResponseRedirect(reverse('get_user', kwargs={'user_name': user.username}))
	
@login_required
def edit_cocktail(request, cocktail_name_slug):
    instance = Cocktail.objects.get(slug=cocktail_name_slug)
    if request.user!=instance.author:
            return HttpResponseRedirect(reverse('index'))
    ingredients = instance.ingredient_set.all()
    instructions = instance.instruction_set.all()
    initial_ingr = []
    initial_instr = []
    for i in ingredients:
            initial_ingr.append({'name': i.name, 'type': i.type, 'quantity': i.quantity})
    for i in instructions:
            initial_instr.append({'text': i.text})
    cocktail_form = CocktailForm(request.POST or None, instance=instance)
    ingredientSet = IngredientFormSet(request.POST or None, initial=initial_ingr, prefix="fs1")
    instructionSet = InstructionFormSet(request.POST or None, initial=initial_instr, prefix="fs2")
    context_dict = {}
    context_dict['cocktail_form'] = cocktail_form
    context_dict['ingredientSet'] = ingredientSet
    context_dict['instructionSet'] = instructionSet
    if cocktail_form.is_valid() and ingredientSet.is_valid() and instructionSet.is_valid():
        cocktail = cocktail_form.save()
        cocktail.ingredient_set.all().delete()
        cocktail.instruction_set.all().delete()
        ingredientSet = ingredientSet.cleaned_data
        print ingredientSet
        for i in ingredientSet:
                if bool(i):
                        print "hui"
                        temp = Ingredient.objects.get_or_create(quantity=i['quantity'], name=i['name'])
                        ingredient = temp[0]
                        if (temp[1]):
                                ingredient.type = i['type']				
                                ingredient.cocktails.add(cocktail)
                                ingredient.save()
        instructionSet = instructionSet.cleaned_data
        for i in instructionSet:
                if bool(i):
                        instruction = Instruction.objects.get_or_create(cocktail=cocktail, text=i['text'])[0]
                        instruction.save()
        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'cocktails/upload_cocktail.html', context_dict) 
