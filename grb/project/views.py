import json
import time
import urllib.request
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Recipe
from .forms import AddRecipe

def addRecipe(request):
    if request.method == "POST":
        form = AddRecipe(request.POST)

        if form.is_valid():
            newRecipe = Recipe(title = form.cleaned_data['title'],
                               ingredients = form.cleaned_data['ingredients'],
                               instructions = form.cleaned_data['instructions'],
                               prepMinutes = form.cleaned_data['prepMinutes'],
                               cookMinutes = form.cleaned_data['cookMinutes'],
                               servings = form.cleaned_data['servings']
                               )
            newRecipe.save()

            return HttpResponseRedirect(f"/viewRecipe/{newRecipe.id}")
        else:
            pass # TODO - Show error

    else:
        form = AddRecipe()

        form.fields['ingredients'].initial = "Separate by line breaks.\nOn each line: Quantity, Unit, Ingredient"
        form.fields['instructions'].initial = "Separate by line breaks."

        return render(request, "addRecipe.html", {
            "form": form
        })

def viewRecipe(request, id):
    recipe = Recipe.objects.get(pk=id)
    formattedIngredients = recipe.getIngredients()
    formattedInstructions = recipe.getInstructions()
    prepTime = recipe.convert_mins_to_hhmm(recipe.prepMinutes)
    cookTime = recipe.convert_mins_to_hhmm(recipe.cookMinutes)
    combinedTime = recipe.combine_times()

    return render(request, "viewRecipe.html", {
        "recipe": recipe,
        "formattedIngredients": formattedIngredients,
        "formattedInstructions": formattedInstructions,
        "prepTime": prepTime,
        "cookTime" : cookTime,
        "combinedTime" : combinedTime
    })

def browseRecipe(request, tags=None):
    recipes = Recipe.objects.all() # TODO add filtering

    return render(request, "browseRecipes.html", {
        "recipes": recipes
    })

def deleteRecipe(request, id):
    Recipe.objects.filter(pk=id).delete()
    # SomeModel.objects.filter(id=id).delete()
    recipes = Recipe.objects.all()
    return render(request, "browseRecipes.html", {
        "recipes": recipes
    })