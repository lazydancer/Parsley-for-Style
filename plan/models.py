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

class Ingredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	amount = models.FloatField()
	unit = models.CharField(max_length=100)
	cost = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return self.name



	

		
