from .models import Recipe

def crud_add_recipe(recipe_dict):
    tags = recipe_dict.pop('tags')
    recipe = Recipe(**recipe_dict)
    recipe.save()
    recipe.tags.add(*tags)
    return recipe.id

def crud_edit_recipe(prev_id, recipe_dict):
    tags = recipe_dict.pop('tags')
    recipe = Recipe.objects.get(id=prev_id)
    for key, val in recipe_dict.items():
        setattr(recipe, key, val)
    recipe.save()
    recipe.tags.set(tags)
    return recipe.id

def crud_get_recipes(id = -1, tags = ()):
    # If provided a single ID, return it
    if id != -1:
        return Recipe.objects.filter(id=id)[0]

    # If provided a list of tags
    if tags:
        return Recipe.objects.filter(tags__name__in = tags)

    # Otherwise, return all
    return Recipe.objects.all()

def crud_delete_recipe(id):
    Recipe.objects.filter(pk=id).delete()
    return id