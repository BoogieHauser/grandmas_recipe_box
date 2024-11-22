import json
import time
import urllib.request
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Recipe
from .forms import AddRecipe

def addRecipe(request, prev_id=-1):
    # If we have submitted data inside a form to add or edit a recipe

    if request.method == "POST":
        form = AddRecipe(request.POST)

        if form.is_valid():
            # TODO Add new recipe vs edit?
            print(f'form: {form}')
            print(f'cleaned:{form.cleaned_data}')

            # check if id exists in db
            #     update
            # else
            #     new entry
            if form.cleaned_data['prev_id'] == -1:
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
                prevRecipe = Recipe.objects.get(id=form.cleaned_data['prev_id'])
                prevRecipe.title = form.cleaned_data['title']
                prevRecipe.ingredients = form.cleaned_data['ingredients']
                prevRecipe.instructions = form.cleaned_data['instructions']
                prevRecipe.prepMinutes = form.cleaned_data['prepMinutes']
                prevRecipe.cookMinutes = form.cleaned_data['cookMinutes']
                prevRecipe.servings = form.cleaned_data['servings']
                prevRecipe.save()

                return HttpResponseRedirect(f"/viewRecipe/{prevRecipe.id}")

        else:
            # Ideally we'd provide the user an opportunity to fix their error with minimal re-typing
            pass # TODO - Show error

    else:
        # The GET route - Loading a form and pre-populating data (i editing) or instructions (if a new recipe)
        form = AddRecipe()

        # If id is not negative one, it was specified in the URL.  Use the ID specified in the URL to pre-populate
        # the form (simulating an edit with as much information as possible pre-provided)
        if prev_id != -1:
            prevRecipe = Recipe.objects.get(id=prev_id)
            form.fields['title'].initial = prevRecipe.title
            form.fields['ingredients'].initial = prevRecipe.ingredients
            form.fields['instructions'].initial = prevRecipe.instructions
            form.fields['prepMinutes'].initial = prevRecipe.prepMinutes
            form.fields['cookMinutes'].initial = prevRecipe.cookMinutes
            form.fields['servings'].initial = prevRecipe.servings

        # If the id is negative one, it was not specified in the URL.  Here we pre-populate the form only with
        # syntax instructions for ingredient and instruction fields
        else:
            form.fields['ingredients'].initial = "Separate by line breaks.\nOn each line: Quantity, Unit, Ingredient"
            form.fields['instructions'].initial = "Separate by line breaks."

        # Return the form to be completed by the user
        return render(request, "addRecipe.html", {
            "form": form,
            "prev_id": prev_id
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