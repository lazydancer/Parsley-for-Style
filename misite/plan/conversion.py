from .models import Recipe, Ingredient

def combine(ingredient_list):
	
	result = []
	for item in ingredient_list:
		componentInResults = len([x for x in result if x.component == item.component]) > 0
		componentList = [x for x in ingredient_list if x.component == item.component]
		if len(componentList) > 0 and not componentInResults:	
			result.append(addAmounts(componentList))  

	return result


def friendlyUnits(ingredient_list):
	
	result = []

	for ingredient in ingredient_list:
		
		common_unit = ingredient.component.common_unit
		
		if common_unit == "default":
			ml = ingredient.amount / ingredient.component.density
			
			amount,unit = gramsToTeaCups(ml)

			ingredient.amount = amount			
			ingredient.unit = unit
			result.append(ingredient)

		else:
			unit_list = ingredient.component.unit_set.all()
			
			for unit in unit_list:
				if unit.name == common_unit:
					
					ingredient.amount = ingredient.amount / unit.amount
					ingredient.unit = common_unit
					result.append(ingredient)
					
	return result


convML = {
 	'cup': 284.13,
	'tbsp': 17.75,
	'tsp': 5.91,
	'dash': 1,
}
convG = {
	'lb': 453.6,
	'oz': 28.34,
	'pinch': 2,
}

def conversionToGram(ingredient):

	aunit = ingredient.unit
	density = ingredient.component.density

	common_unit = ingredient.component.common_unit
	unit_list = ingredient.component.unit_set.all()

	for unit in unit_list:
		if unit.name == common_unit:
			return unit.amount	

	if aunit in convG:
		return convG[aunit]

	if aunit in convML:
		return convML[aunit] * density

	#print(aunit," does not exist")
	return 10

def addAmounts(y):
	result = y[0]

	total_amount = 0
	for i in y:
		total_amount += i.amount * conversionToGram(i)
	
	result.amount = total_amount
	result.unit = "g"
	
	return result

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
		return (round(cups/0.25)*0.25, "cup")