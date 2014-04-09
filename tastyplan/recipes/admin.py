from django.contrib import admin
from recipes.models import *

class NutritientQuantityInline(admin.TabularInline):
  	model = NutrientQuantity
  	extra = 3

class IngredientInline(admin.TabularInline):
 	model = Ingredient
 	extra = 3

class FoodAdmin(admin.ModelAdmin):
  	inlines = [NutritientQuantityInline]

class RecipeAdmin(admin.ModelAdmin):
  	inlines = [IngredientInline]

admin.site.register(Nutrient)
admin.site.register(Food, FoodAdmin)
admin.site.register(Recipe, RecipeAdmin)
