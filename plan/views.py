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
	elif aunit == "lbs" or aunit == "lb" or aunit == "lb.":
		return 453.6
	elif aunit == "oz" or aunit == "oz.":
		return 28.34
	elif aunit == "pinch" or aunit == "Pinch":
		return 3

	# These are too fill to not let the program fail
	else:
		print(aunit," does not exist")
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

def convertToML(ingredients):
	result = []

	for ingredient in ingredients:
		if ingredient.component.common_unit == "default":
			ml = gramsToML(ingredient.amount, ingredient.component.density)
			amount,unit = gramsToTeaCups(ml)
			ingredient.amount = amount			
			ingredient.unit = unit
			result.append(ingredient)

	return result

def gramsToML(grams, density):
	return grams/density

def roundPartial (value, resolution):
	return round(value/resolution) * resolution

def gramsToTeaCups(ml):
	if ml < 2:
		return (1, "dash")
	elif ml < 5:
		return (0.5, "tsp")
	elif ml < 10: 
		return (1, "tsp")
	elif ml < 16:
		return (2, "tsp")
	elif ml < 30:
		return (1, "tbsp")
	elif ml < 48:
		return (2, "tbsp")
	elif ml < 64:
		return (3, "tbsp")
	else:
		cups = ml/284
		return (roundPartial(cups,0.25), "cups")

def index(request):
	latest_recipe_list = Recipe.objects.order_by('id')[:5]

	ingredient_list = []
	for recipe in latest_recipe_list:
		for ingredient in recipe.ingredient_set.all():
			ingredient_list.append(ingredient)

	ingredient_list = combineIngredients(ingredient_list)
	ingredient_list = convertToML(ingredient_list)
	ingredient_list = groupbyDepartment(ingredient_list)

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