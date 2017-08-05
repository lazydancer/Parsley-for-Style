from django.db import models


class Recipe(models.Model):
	title = models.CharField(max_length=100)
	summary = models.CharField(max_length=500)
	preptime = models.IntegerField()
	cooktime = models.IntegerField()
	servings = models.IntegerField()
	instruction = models.CharField(max_length=1400)

	def decode_instruction(self):
		return self.instruction.split("#,#")

	def __str__(self):
		return self.title

class Component(models.Model):
	name = models.CharField(max_length=100)
	density = models.FloatField() # g/cm3 or g/mL
	cost = models.DecimalField(max_digits=6, decimal_places=2) # CAD/kg
	department = models.CharField(max_length=100)
	common_unit = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Ingredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	component = models.ForeignKey(Component, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	amount = models.FloatField()
	unit = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name

class Unit(models.Model):
	component = models.ForeignKey(Component, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	amount = models.FloatField() # in grams
		