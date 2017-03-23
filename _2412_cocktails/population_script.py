import os, time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_2412_cocktails.settings')

import django
django.setup()
from cocktails.models import *
from django.core.files import File

def populate():
	
	u = add_user("test", "password123", "2017-03-23")
	for user in users:
		test = add_user(user, "password123", "1987-02-28")
		test.userprofile.follows.add(u.userprofile)

	for cocktail in menu:
		c = add_cocktail(cocktail, menu[cocktail]["rating"], u, menu[cocktail]["picture"])
		for ingredient in menu[cocktail]["ingredients"]:
			add_ingredient(c, ingredient[0], ingredient[1], ingredient[2])
		for instruction in menu[cocktail]["instructions"]:
			add_instruction(c, instruction)
		time.sleep(0.5)
		

	for c in Cocktail.objects.all():
		for i in Instruction.objects.filter(cocktail=c):
			print "- {0} - {1}".format(str(c), str(i))
		for n in c.ingredient_set.all():
			print "- {0} - {1}".format(str(c), str(n))


def add_user(username, password, dob):
	temp = User.objects.get_or_create(username=username)
	u = temp[0]
	u.set_password(password)
	u.save()
	
	if temp[1]:
		p = UserProfile()
		p.dob=dob
		p.user=u
	else:
		p = u.userprofile
		p.dob=dob
	p.save()
	return u

def add_cocktail(name, rating, user, picture):
	c = Cocktail.objects.get_or_create(name=name)[0]
	c.rating = rating
	c.author = user
	path = "cocktail_images/" + picture
	c.picture = path
	c.save()
	return c

def add_ingredient(cock, quan, name, type):
	i = Ingredient.objects.get_or_create(quantity=quan, name=name)[0]
	i.cocktails.add(cock)
	i.type=type
	i.save()
	return i

def add_instruction(cock, instr):
	i = Instruction.objects.get_or_create(cocktail=cock, text=instr)[0]
	i.save()

users = ["Vincent", "Deadward", "LilVinnie", "JohnCena"] 

menu = { 
		"Mojito" : { 
			"ingredients" : [
				["2 parts", "white rum", "alcoholic"],
				["1/2", "fresh lime", "fruit"],
				["12 leaves", "fresh mint", "herb"],
				["2 heaped bar spoons", "casted sugar", "condiment"],
				["dash", "soda water", "non-alcoholic"],
				["cubed", "ice", "non-alcoholic"],
				["crushed", "ice", "non-alcoholic"],
				["sprig", "fresh mint", "herb"],],
			"instructions" : [
				"Put the four lime wedges into a glass.",
				"Add 2 heaped bar spooons of casted sugar and muddle(squish everything together) to release the lime juice.",
				"Put 12 mint leaves on one hand and clap. This bruises the leaves and releases the aroma.",
				"Rub the mint leaves around the rim of the glass and drop them in. Use a bar spoon to gently push the mint down into the lime juice.",
				"Half fill the glass with crushed ice and pour in the 2 parts of White Rum.",
				"Stir the mix together until the sugar dissolves.",
				"Top up with crushed ice, a splash of the soda water and garnish it with a sprig of mint.",],
			"rating" : 4.9,
			"picture": "mojito.jpg"},
		"Bloody Mary" : {
			"ingredients" : [
				["2 parts", "Vodka", "alcoholic"],
				["4 parts", "tomato juice", "non-alcoholic"],
				["1/2 part", "lemon juice", "non]"],
				["4 dashes", "Worcestershire sauce", "non-alcoholic"],
				["4 dashes", "Tabasco", "non-alcoholic"],
				["pinch", "sea salt", "condiment"],
				["pinch", "black pepper", "condiment"],
				["cubed", "ice", "non-alcoholic"],],
			"instructions" : [
				"Add plenty of ice and all of your ingredients to a shaker or stirring glass (Vodka, tomato juice, lemon juice, Worcestershire sauce, Tabasco(*), salt and pepper).",
				"If you're using a shaker, tilt it backwards and forwards a few times to mix the ingredients without making the drink frothy. If you're stirring, you can do so vigorously",
				"Pour the mix into a glass. Top up with fresh ice if it's not quite full.",
				"Add your garnishes. Any fresh herbs and a celery stick work well.",
				"* if you're making Bloody Marys for a group of people, make a jug without spice and let people add their own Tabasco. Some like it hot, others not so much!",],
			"rating" : 4.2,
			"picture": "bloodymary.jpg"},
			
		"Passionfruit Margarita" : {
			"ingredients" : [
				["a lot of", "Tequila", "alcoholic"],
				["some", "Passionfruit syrup", "non-alcoholic"],
				["a little", "Fresh lime juice", "non-alcoholic"],
				["a tiny bit of", "sugar rim", "non-alcoholic"],],
			"instructions" : [
				"Chill a cocktail glass with crushed ice",
				"Add all ingredients to a Boston glass and shake with cubed ice",
				"Remove crushed ice, rim the glass with sugar",
				"Strain the mixture into the glass",],
			"rating" : 3.56,
			"picture": "passionfruit_margarita.jpg"},
			
		"Manhattan" : {
			"ingredients" : [
				["100 ml", "Whiskey", "alcoholic"],
				["50 ml", "Sweet vermouth", "alcoholic"],
				["dash", "Aromatic bitters", "alcoholic"],],
			"instructions" : [
				"Chill a cocktail glass with ice",
				"Add the ingredients and stir until the outside of the Boeston glass clouds up with the chill",
				"Remove chilling ice and strain into cocktail glass. Garnish with a cocktail cherry",],
			"rating" : 3.71,
			"picture" : "manhattan.jpg"},
			
		"Cosmopolitan" : {
			"ingredients" : [
				["50 ml", "Vodka", "alcoholic"],
				["10 ml", "Cointreau", "alcoholic"],
				["30 ml", "Lime Juice", "non-alcoholic"],
				["30 ml", "Cranberry Juice", "non-alcoholic"],],
			"instructions" : [
				"Chill a cocktail glass with crushed ice",
				"Add all ingredients to a Boston glass and shake with cubed ice",
				"Remove crushed ice and strain the mixture into the glass",
				"Take a slice of orange rind, hold it between the thumb and forefinger over the glass in front of a ligther flame and squeeze the orange rind quickly. This should light the zest and create an awesome aroma above the cocktail.",],
			"rating" : 2.2,
			"picture" : "cosmopolitan.jpg"},
			
		"Raspberry Lynchburg" : {
			"ingredients" : [
				["50 ml", "Whiskey", "alcoholic"],
				["10 ml", "Chambord", "alcoholic"],
				["10g", "Raspberry puree", "fruit"],
				["30 ml", "Lemon Juice", "non-alcoholic"],
				["1", "Egg white", "food"],
				["50 ml", "Lemonade", "non-alcoholic"],],
			"instructions" : [
				"Fill a long glass with cubed ice",
				"Add all ingredients except the lemonade to a Boston glass",
				"Shake the ingredients (without ice) and pour over cubed ice",
				"Top with lemonade",
				"Garnish with a lemon wedge and a straw",],
			"rating": 2.8,
			"picture" : "raspberry_lynchburg.jpg"},

		"Coco Italiano" : {
			"ingredients" : [
				["50 ml", "Tequila", "alcoholic"],
				["10 ml", "Campari", "alcoholic"],
				["25 ml", "Martini Rosso", "alcoholic"],
				["30 ml", "Coconut Syrup", "non-alcoholic"],],
			"instructions" : [
				"Add all the ingredients to a mixing glass and stir until the glass clouds us",
				"Strain into a chilled Nick & Nora glass",],
			"rating" : 4.13,
			"picture" : "coco_italiano.jpg"},
		}
	
	
if __name__ == '__main__':
	print("Starting Population script...")
	populate()