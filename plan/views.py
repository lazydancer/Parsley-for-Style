from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Recipe, Ingredient


def conversionToGram(aunit, density):
	if aunit == "cup" or aunit == "cups":
		return density * 284.13
	elif aunit == "Tbsp" or aunit == "tbsp":
		return density * 17.75
	elif aunit == "tsp" or aunit == "Tsp":
		return density * 5.91
	elif aunit == "lbs" or aunit == "lb":
		return 453.6
	elif aunit == "oz" or aunit == "oz.":
		return 28.34

	# These are too fill to not let the program fail
	else:
		return 10

def combineIngredientComponents(y):

	a = y[0]

	total_amount = 0
	for i in y:
		amount = i.amount * conversionToGram(i.unit, i.component.density)
		total_amount += amount

	a.amount = total_amount
	a.unit = "g"
	
	return a
	

def combineIngredients(ingredient_list):
	doneIngredients = []
	for item in ingredient_list:
		if len([x for x in doneIngredients if x.component == item.component]) == 0:	
		# Check if the component has already been covered, if so skip to the next 
			y =  [x for x in ingredient_list if x.component == item.component]
			if len(y) >= 1:
				a = combineIngredientComponents(y)
				doneIngredients.append(a)  

	return doneIngredients

def index(request):
	latest_recipe_list = Recipe.objects.order_by('id')[:5]

	ingredient_list = []
	for recipe in latest_recipe_list:
		for ingredient in recipe.ingredient_set.all():
			ingredient_list.append(ingredient)

	ingredient_list = combineIngredients(ingredient_list)
	

	context = {
		'latest_recipe_list': latest_recipe_list,
		'ingredient_list': ingredient_list,
	}

	return render(request, 'plan/index.html', context)
'''
class IndexView(generic.ListView):
	template_name = 'plan/index.html'
	context_object_name = 'latest_recipe_list'

	def get_queryset(self):
		return Recipe.objects.order_by('id')[:5]
'''
class DetailView(generic.DetailView):
	model = Recipe
	template_name = 'plan/detail.html'