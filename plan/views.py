import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.core import serializers
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
	

	# Store most recent 5 if first time, else open the session results
	recipe_list = Recipe.objects.order_by('id')[:5]
	recipes_id = [recipe.id for recipe in recipe_list]
	recipes_id = request.session.get('recipe_list', recipes_id)
	request.session['recipe_list'] = recipes_id

	
	recipe_list = Recipe.objects.filter(pk__in=recipes_id)

	

	ingredient_list = []
	for recipe in recipe_list:
		for ingredient in recipe.ingredient_set.all():
			ingredient_list.append(ingredient)

	ingredient_list = combine(ingredient_list)
	ingredient_list = friendlyUnits(ingredient_list)
	ingredient_list = groupbyDepartment(ingredient_list)

	ingredient_list = request.session.get('ingredient_list', ingredient_list)
	

	# session test, number of visits
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits+1

	context = {
		'latest_recipe_list': recipe_list,
		'ingredient_list': ingredient_list,
		'num_visits' : num_visits,
	}

	return render(request, 'plan/index.html', context)

class DetailView(generic.DetailView):
	model = Recipe
	template_name = 'plan/detail.html'

class RecipeListView(generic.TemplateView):
	model = Recipe
	template_name = 'plan/add-recipe.html'

	def get_context_data(self, **kwargs):
		context = super(RecipeListView, self).get_context_data(**kwargs)
		context['latest'] = Recipe.objects.order_by('id')[:8]
		return context

def addRecipe(request):
	print(request.session['recipe_list'])
	request.session['recipe_list'].append(6)

	return(index(request))