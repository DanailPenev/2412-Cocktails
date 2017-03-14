from django.contrib import admin
from cocktails.models import *

class CocktailAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(Ingredient)
admin.site.register(Instruction)
admin.site.register(UserProfile)
# Register your models here.
