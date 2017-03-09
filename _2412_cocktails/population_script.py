import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_2412_cocktails.settings')

import django
django.setup()
from cocktails.models import *

def populate():

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
				"Top up with crushed ice, a splash of the soda water and garnish it with a sprig of mint.",]},
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
				"* if you're making Bloody Marys for a group of people, make a jug without spice and let people add their own Tabasco. Some like it hot, others not so much!",]}}


	for cocktail in menu:
		c = add_cocktail(cocktail)
		for ingredient in menu[cocktail]["ingredients"]:
			add_ingredient(c, ingredient[0], ingredient[1], ingredient[2])
		for instruction in menu[cocktail]["instructions"]:
			add_instruction(c, instruction)

	for c in Cocktail.objects.all():
		for i in Instruction.objects.filter(cocktail=c):
			print "- {0} - {1}".format(str(c), str(i))
		for n in c.ingredient_set.all():
			print "- {0} - {1}".format(str(c), str(n))




def add_cocktail(name):
	c = Cocktail.objects.get_or_create(name=name)[0]
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


if __name__ == '__main__':
	print("Starting Population script...")
	populate()