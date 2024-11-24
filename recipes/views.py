import json
import time
import urllib.request
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from wheel.cli import tags_f

from .models import Recipe
from .forms import RecipeForm

def addRecipe(request, prev_id=-1):
    # If we have submitted data inside a form to add or edit a recipe

    form = RecipeForm(request.POST)
    print(form)
    print(form.is_valid())
    if request.method == "POST":

        if form.is_valid():
            # TODO Add new recipe vs edit?

            print(f'form: {form}')
            print(f'cleaned:{form.cleaned_data}')

            # if form.cleaned_data['id'] == -1:
            if 'id' not in form.cleaned_data:
                newRecipe = form.save(commit=False)
                newRecipe.save()
                form.save_m2m()

                return HttpResponseRedirect(f"/viewRecipe/{newRecipe.id}")

            else:
                prevRecipe = Recipe.objects.get(id=form.cleaned_data['id'])
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
        # The GET route - Loading a form and pre-populating data (if editing) or instructions (if a new recipe)
        #form = AddRecipe()

        # If id is not negative one, it was specified in the URL.  Use the ID specified in the URL to pre-populate
        # the form (simulating an edit with as much information as possible pre-provided)

        if prev_id != -1:
            prevRecipe = Recipe.objects.get(id=prev_id)
        #     form.fields['title'].initial = prevRecipe.title
        #     form.fields['ingredients'].initial = prevRecipe.ingredients
        #     form.fields['instructions'].initial = prevRecipe.instructions
        #     form.fields['prepMinutes'].initial = prevRecipe.prepMinutes
        #     form.fields['cookMinutes'].initial = prevRecipe.cookMinutes
        #     form.fields['servings'].initial = prevRecipe.servings

        # If the id is negative one, it was not specified in the URL.  Here we pre-populate the form only with
        # syntax instructions for ingredient and instruction fields
        else:
            prevRecipe = None
        #     form.fields['ingredients'].initial = "Separate by line breaks.\nOn each line: Quantity, Unit, Ingredient"
        #     form.fields['instructions'].initial = "Separate by line breaks."

        # Return the form to be completed by the user
        return render(request, "addRecipe.html", {
            "form": form,
            "id": prev_id,
            "prevRecipe": prevRecipe
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