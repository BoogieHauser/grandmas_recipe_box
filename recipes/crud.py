from .models import Recipe

def crud_add_recipe(recipe_dict):
    tags = recipe_dict.pop('tags')
    recipe = Recipe(**recipe_dict)
    recipe.save()
    recipe.tags.add(*tags)
    return recipe.id