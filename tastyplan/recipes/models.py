from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators
#https://django-durationfield.readthedocs.org/en/latest/
from durationfield.db.models.fields.duration import DurationField

class Recipe(models.Model):
  url = models.URLField(unique=True, help_text="The absolute URL of this recipe.")
  name = models.CharField(max_length=254, help_text="The name of this recipe.")
  servings = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1)], help_text="The number of servings this recipe makes.")
  ingredients = models.ManyToManyField("Food", through='Ingredient', help_text="The ingredients and their quantities in this recipe.")
  DIFFICULTY_CHOICES = (
      (1, 'Very easy'),
      (2, 'Easy'),
      (3, 'Medium'),
      (4, 'Difficult'),
      (5, 'Very difficult')
  )
  difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, blank=True, help_text="The difficulty of this recipe (optional).")
  time = DurationField(blank=True, help_text="The time required to prepare and cook this recipe (optional).")
  method = models.TextField(blank=True, help_text="The description for how to cook this recipe (optional).")

class Food(models.Model):
  #ingredient["meta"]["ndb_no"] is unique ref in usda
  group = models.CharField(max_length=254, help_text="The food group this food belongs to.")
  name = models.CharField(db_index=True, max_length=254, help_text="The name of this food.")
  common_name = models.CharField(db_index=True, max_length=254, help_text="The common name of this food (optional).")
  nutrients = models.ManyToManyField("Nutrient", through='NutrientQuantity', help_text="The nutritional content of 100g of this food.")

class Nutrient(models.Model):
  #nutrient["code"] and nutrient["name"]+nutrient["units"] are unique refs in usda
  name = models.CharField(max_length=254, help_text="The name of this nutrient.")
  units = models.CharField(max_length=254, help_text="The units this nutrient is measured in.")

class NutrientQuantity(models.Model):
  nutrient = models.ForeignKey("Nutrient", help_text="The nutrient this nutritional information matches.")
  food = models.ForeignKey("Food", help_text="The food this nutritional information matches.")
  quantity = models.DecimalField(max_digits=10, decimal_places=5, help_text="The matched nutrient's quantity in its units contained in the matched food.")

class Ingredient(models.Model):
  recipe = models.ForeignKey("Recipe", help_text="The recipe this ingredient is found in.")
  food = models.ForeignKey("Food", help_text="The food this ingredient matched.")
  description = models.CharField(max_length=254, help_text="The full description of this ingredient.")
  parsed_name = models.CharField(max_length=254, help_text="The parsed name of this ingredient.")
  parsed_nouns = models.CharField(max_length=254, help_text="The parsed nouns of this ingredient.")
  parsed_quantity = models.CharField(max_length=254, help_text="The parsed quantity of this ingredient.")
  converted_quantity = models.DecimalField(max_digits=6, decimal_places=3, validators=[validators.MinValueValidator(0)], help_text="This ingredient's quantity in 100g units.")
