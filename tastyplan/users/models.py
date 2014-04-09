from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators

class User(models.Model):
	profile = models.ForeignKey("Profile", help_text="The profile of this user.")
	demographics = models.ForeignKey("Demographics", help_text="The demographic profile of this user.")
	nutritional_requirements = models.ForeignKey("NutritionalRequirements", help_text="The nutritional requirements of this user.")
	ratings = models.ManyToManyField("recipes.Recipe", through="Rating", help_text="The ratings this user assigned to recipes.")

class Profile(models.Model):
	first_name = models.CharField(max_length=254, help_text="The first name of this user.")
	last_name = models.CharField(max_length=254, help_text="The first name of this user.")
	email = models.EmailField(unique=True, max_length=254, help_text="The email address of this user.")
	username = models.SlugField(unique=True, help_text="The username of this user.")

class Demographics(models.Model):
	age = models.PositiveSmallIntegerField(help_text="The age of this user.")
	height = models.PositiveSmallIntegerField(help_text="The height of this user (in cm).")
	weight = models.PositiveSmallIntegerField(help_text="The weight of this user (in kg).")

class NutritionalRequirements(models.Model):
	portions = models.DecimalField(default=1, max_digits=3, decimal_places=1, help_text="The number of servings this user prefers to eat.")
	nutrients = models.ManyToManyField("recipes.Nutrient", through="NutritionalRequirementsRange", help_text="The quantities of nutrients required by this user.")
	forbidden_foods = models.ManyToManyField("recipes.Food")

class Log(models.Model):
	date = models.DateField(auto_now_add=True, help_text="The date this log was created.")
	recipes = models.ManyToManyField("recipes.Recipe", through="Portions", help_text="The recipes and portions suggested and eaten on the date of this log.")
	user = models.ForeignKey("User", help_text="The user this log refers to.")
	demographics = models.ForeignKey("Demographics", help_text="The demographic information of the user on the date of this log.")
	nutritional_requirements = models.ForeignKey("NutritionalRequirements", help_text="The nutritional requirements of the user on the date of this log.")

class Rating(models.Model):
	user = models.ForeignKey("User", help_text="The user who made this rating.")
	recipe = models.ForeignKey("recipes.Recipe", help_text="The recipe this rating refers to.")
	rating = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)], help_text="The rating this user gave to the recipe.")

class NutritionalRequirementsRange(models.Model):
	nutritional_requirements = models.ForeignKey("NutritionalRequirements", help_text="The nutritional requirements which contain this range.")
	nutrient = models.ForeignKey("recipes.Nutrient", help_text="The nutrient these requirements refer to.")
	quantity = models.DecimalField(max_digits=10, decimal_places=5, help_text="The minimum required quantity of this nutrient by the user.")

class Portions(models.Model):
	log = models.ForeignKey("Log", help_text="The log these recipe portions apply to.")
	recipe = models.ForeignKey("recipes.Recipe", help_text="The recipe these portions refer to.")
	portions_suggested = models.DecimalField(default=1, max_digits=3, decimal_places=1, help_text="The portions of the recipe suggested")
	portions_eaten = models.DecimalField(default=1, max_digits=3, decimal_places=1, help_text="The portions of the recipe eaten")
