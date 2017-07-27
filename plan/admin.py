from django.contrib import admin

from .models import Recipe, Ingredient

class UnitInline(admin.TabularInline):
	model = Ingredient

class IngredientAdmin(admin.ModelAdmin):
	inlines = [
		UnitInline,
	]

admin.site.register(Recipe, IngredientAdmin)
admin.site.register(Ingredient)

# Register your models here.
