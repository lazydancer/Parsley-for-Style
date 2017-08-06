from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Recipe, Ingredient

from plan.conversion import combine, friendlyUnits


def groupbyDepartment(ingredient_list):

	departmentGroups = ["Produce","Deli","Bakery","Dairy","Meat","Frozen","Grocery","Spices"]

	groupedIngredientList = []
	for department in departmentGroups:
		group = []
		for ingredient in ingredient_list:
			if ingredient.component.department == department:
				group.append(ingredient)
		groupedIngredientList.append(group)

	return groupedIngredientList


def index(request):
	latest_recipe_list = Recipe.objects.order_by('id')[:5]

	ingredient_list = []
	for recipe in latest_recipe_list:
		for ingredient in recipe.ingredient_set.all():
			ingredient_list.append(ingredient)

	ingredient_list = combine(ingredient_list)
	ingredient_list = friendlyUnits(ingredient_list)

	ingredient_list = groupbyDepartment(ingredient_list)

	context = {
		'latest_recipe_list': latest_recipe_list,
		'ingredient_list': ingredient_list,
	}

	return render(request, 'plan/index.html', context)

class DetailView(generic.DetailView):
	model = Recipe
	template_name = 'plan/detail.html'