from django.contrib import admin
from users.models import *

class RatingInline(admin.TabularInline):
  	model = Rating
  	extra = 3

class NutritionalRequirementsRangeInline(admin.TabularInline):
 	model = NutritionalRequirementsRange
 	extra = 3

class PortionsInline(admin.TabularInline):
 	model = Portions
 	extra = 3

class UserAdmin(admin.ModelAdmin):
  	inlines = [RatingInline]

class NutritionalRequirementsAdmin(admin.ModelAdmin):
  	inlines = [NutritionalRequirementsRangeInline]

class LogAdmin(admin.ModelAdmin):
  	inlines = [PortionsInline]

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Demographics)
admin.site.register(NutritionalRequirements, NutritionalRequirementsAdmin)
admin.site.register(Log, LogAdmin)
