from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Recipe

def crud_add_recipe(recipe_dict):
    tags = recipe_dict.pop('tags')
    recipe = Recipe(**recipe_dict)
    recipe.save()
    recipe.tags.add(*tags)
    return recipe.id

def crud_edit_recipe(prev_id, recipe_dict):
    include_tags = False
    if 'tags' in recipe_dict:
        include_tags = True
        tags = recipe_dict.pop('tags')
    recipe = Recipe.objects.get(id=prev_id)
    for key, val in recipe_dict.items():
        setattr(recipe, key, val)
    recipe.save()
    if include_tags:
        recipe.tags.set(tags)
    return recipe.id

def crud_get_recipes(id = -1, tags = (), query = "", user = None):
    # If provided a single ID, return it
    if id != -1:
        # Should throw a 404 if the recipe does not exist
        matches = Recipe.objects.filter(id=id)

        if len(matches) == 0:
            raise Http404("Recipe not found")
        else:
            matched_recipe = matches[0]

        # Should throw a 500 if the user does not have permission to see the recipe
        # (is recipe owner or the recipe is public)
        if matched_recipe.user != user and not matched_recipe.public:
            raise PermissionDenied

        return matched_recipe

    # If provided a list of tags
    if tags:
        return Recipe.objects.filter(tags__name__in = tags).filter(Q(user = user) | Q(public = True))

    # If provided a query
    if query:
        return Recipe.objects.filter(title__icontains = query).filter(Q(user = user) | Q(public = True))

    # Otherwise, return all
    return Recipe.objects.filter(Q(user = user) | Q(public = True))

def crud_delete_recipe(id):
    Recipe.objects.filter(pk=id).delete()
    return id