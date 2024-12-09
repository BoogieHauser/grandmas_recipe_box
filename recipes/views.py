
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Recipe
from .forms import RecipeForm
from .crud import crud_add_recipe, crud_edit_recipe, crud_delete_recipe, crud_get_recipes


def addRecipe(request, prev_id=-1):
    # If we have submitted data inside a form to add or edit a recipe
    form = RecipeForm(request.POST, request.FILES)
    if request.method == "POST":

        # print(form)
        print(form.data)
        # print(form.errors)
        # print(form.is_valid())
        # print(form.cleaned_data)
        # print(request.FILES.get("image"))

        # Check if form is valid
        if form.is_valid():

            # The hidden field is not present in cleaned_data, so we pull it from data
            provided_id = form.data.get('id', -1)

            # This is a new recipe
            if int(provided_id) == -1:
                id = crud_add_recipe(form.cleaned_data)

            # Editing an existing recipe
            else:
                if form.data.get('maintain-image', 'Remove Image') == 'Keep Image':
                     form.cleaned_data.pop('image')
                id = crud_edit_recipe(provided_id, form.cleaned_data)

            return HttpResponseRedirect(f"/viewRecipe/{id}")

        # Form is not valid
        else:
            return HttpResponseRedirect(f"/")

    elif request.method == "GET":
        # The GET route - Loading a form and pre-populating data (if editing) or instructions (if a new recipe)
        #form = AddRecipe()

        # If id is not negative one, it was specified in the URL.  Use the ID specified in the URL to pre-populate
        # the form (simulating an edit with as much information as possible pre-provided)
        if prev_id != -1:
            prevRecipe = crud_get_recipes(id = prev_id)
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
    recipe = crud_get_recipes(id = id)
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

def browseRecipe(request):
    # Filter by tag
    tags = request.GET.get('tags', None)

    if tags:
        # TODO only works for one tag
        tags = [tags.strip('[]')]
        recipes = crud_get_recipes(tags = tags)

    else:
        recipes = crud_get_recipes()

    return render(request, "browseRecipes.html", {
        "recipes": recipes
    })

def deleteRecipe(request, id):
    crud_delete_recipe(id)
    recipes = Recipe.objects.all()
    return render(request, "browseRecipes.html", {
        "recipes": recipes
    })