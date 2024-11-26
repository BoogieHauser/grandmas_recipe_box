
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Recipe
from .forms import RecipeForm

def addRecipe(request, prev_id=-1):
    # If we have submitted data inside a form to add or edit a recipe
    form = RecipeForm(request.POST)
    if request.method == "POST":

        # Check if form is valid
        if form.is_valid():

            # The hidden field is not present in cleaned_data, so we pull it from data
            provided_id = form.data.get('id', -1)

            # This is a new recipe
            if provided_id == -1:
                newRecipe = form.save(commit=False)
                newRecipe.save()
                form.save_m2m()

                return HttpResponseRedirect(f"/viewRecipe/{newRecipe.id}")

            # Editing an existing recipe
            else:
                prevRecipe = Recipe.objects.get(id=provided_id)
                prevRecipe.title = form.cleaned_data['title']
                prevRecipe.ingredients = form.cleaned_data['ingredients']
                prevRecipe.instructions = form.cleaned_data['instructions']
                prevRecipe.prepMinutes = form.cleaned_data['prepMinutes']
                prevRecipe.cookMinutes = form.cleaned_data['cookMinutes']
                prevRecipe.servings = form.cleaned_data['servings']
                prevRecipe.save()

                return HttpResponseRedirect(f"/viewRecipe/{prevRecipe.id}")

    elif request.method == "GET":
        # The GET route - Loading a form and pre-populating data (if editing) or instructions (if a new recipe)
        #form = AddRecipe()

        # If id is not negative one, it was specified in the URL.  Use the ID specified in the URL to pre-populate
        # the form (simulating an edit with as much information as possible pre-provided)

        if prev_id != -1:
            prevRecipe = Recipe.objects.get(id=prev_id)
            taglist = prevRecipe.get_formatted_tags()

        # If the id is negative one, it was not specified in the URL.  Here we pre-populate the form only with
        # syntax instructions for ingredient and instruction fields
        else:
            prevRecipe = None
            taglist = None

        # Return the form to be completed by the user
        return render(request, "addRecipe.html", {
            "form": form,
            "id": prev_id,
            "prevRecipe": prevRecipe,
            "tag_list": taglist,
            "common_tags": Recipe.tags.most_common()[:10], # TODO is this limit appropriate?
        })

def viewRecipe(request, id):
    recipe = Recipe.objects.get(pk=id)
    formattedIngredients = recipe.get_formatted_ingredients()
    formattedInstructions = recipe.get_formatted_instructions()
    prepTime = recipe.convert_mins_to_hhmm(recipe.prepMinutes)
    cookTime = recipe.convert_mins_to_hhmm(recipe.cookMinutes)
    combinedTime = recipe.combine_times()
    tags = recipe.get_tag_list()

    return render(request, "viewRecipe.html", {
        "recipe": recipe,
        "formattedIngredients": formattedIngredients,
        "formattedInstructions": formattedInstructions,
        "prepTime": prepTime,
        "cookTime" : cookTime,
        "combinedTime" : combinedTime,
        "tags": tags
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