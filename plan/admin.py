from django.contrib import admin

from .models import Recipe, Ingredient, Component

class UnitInline(admin.TabularInline):
	model = Ingredient

class IngredientAdmin(admin.ModelAdmin):
	inlines = [
		UnitInline,
	]

admin.site.register(Recipe, IngredientAdmin)
admin.site.register(Ingredient)
admin.site.register(Component)

# Register your models here.
