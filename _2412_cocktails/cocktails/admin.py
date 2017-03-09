from django.contrib import admin
from cocktails.models import *

admin.site.register(Cocktail)
admin.site.register(Ingredient)
admin.site.register(Instruction)
admin.site.register(UserProfile)
# Register your models here.
