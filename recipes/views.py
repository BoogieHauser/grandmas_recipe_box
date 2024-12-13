
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .forms import RecipeForm
from .crud import crud_add_recipe, crud_edit_recipe, crud_delete_recipe, crud_get_recipes
from .processing import process_image_dict

@login_required
def addRecipe(request, prev_id=-1):
    # If we have submitted data inside a form to add or edit a recipe
    form = RecipeForm(request.POST, request.FILES)
    if request.method == "POST":

        # print(form)
        # print(form.data)
        # print(form.errors)
        # print(form.is_valid())
        # print(request.FILES.get("image"))

        # Check if form is valid
        if form.is_valid():
            # The hidden field is not present in cleaned_data, so we pull it from data
            provided_id = form.data.get('id', -1)

            # This is a new recipe
            if int(provided_id) == -1:
                id = crud_add_recipe(form.cleaned_data, user = request.user)

            # Editing an existing recipe
            else:
                recipe_dict = process_image_dict(form.data, form.cleaned_data)
                id = crud_edit_recipe(provided_id, recipe_dict, user = request.user)

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
            prevRecipe = crud_get_recipes(id = prev_id, user = request.user)
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
    if request.user.is_authenticated:
        recipe = crud_get_recipes(id = id, user = request.user)
    else:
        recipe = crud_get_recipes(id = id)

    # 404 or 500 should have been thrown if appropriate by crud_get_recipes
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
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    # Filter by tag
    tags = request.GET.get('tags', None)
    query = request.GET.get('query', None)

    if tags:
        # TODO only works for one tag
        tags = [tags.strip('[]')]
        recipes = crud_get_recipes(tags = tags, user = user)

    elif query:
        recipes = crud_get_recipes(query = query, user = user)

    else:
        recipes = crud_get_recipes(user = user)

    return render(request, "browseRecipes.html", {
        "recipes": recipes,
        "query": query,
    })

@login_required
def deleteRecipe(request, id):
    crud_delete_recipe(id, user = request.user)
    recipes = crud_get_recipes(user = request.user)
    return render(request, "browseRecipes.html", {
        "recipes": recipes
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('browseRecipe')  # Redirect to your browse recipes page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')