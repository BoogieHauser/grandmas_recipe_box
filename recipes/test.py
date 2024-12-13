from xml.dom import VALIDATION_ERR
from django.core.exceptions import ValidationError
from django.template.base import kwarg_re

from django.test import TestCase
from .models import Recipe
from taggit.managers import TaggableManager
from .crud import crud_add_recipe, crud_edit_recipe, crud_get_recipes, crud_delete_recipe
from django.urls import reverse

from .processing import process_image_dict
import tempfile


class RecipeTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            title = "Breakfast Cereal",
            ingredients = """8,oz,milk
1,cup,Lucky Charms""",
            instructions = """pour milk
warm it up if needed
pour cereal in""",
            prepMinutes = 5,
            cookMinutes = 1,
            servings = 1,
        )
        self.recipe.tags.add("Quick and Easy", "Vegetarian")

    def test_recipe_creation(self):
        """Test that a Recipe instance is created correctly"""
        self.assertEqual(self.recipe.title, "Breakfast Cereal")
        self.assertEqual(self.recipe.ingredients, """8,oz,milk
1,cup,Lucky Charms""")
        self.assertEqual(self.recipe.instructions, """pour milk
warm it up if needed
pour cereal in""")
        self.assertEqual(self.recipe.prepMinutes, 5)
        self.assertEqual(self.recipe.cookMinutes, 1)
        self.assertEqual(self.recipe.servings, 1)
        # Tag creation is verified later, as this is a custom object querying it is more complex

    def test_clean_line(self):
        self.assertEqual(self.recipe.clean_line("a,b,c"), "a b c")

    def test_get_ingredients_list(self):
        self.assertEqual(self.recipe.get_ingredients_list(), ["8,oz,milk", "1,cup,Lucky Charms"])

    def test_get_formatted_ingredients(self):
        self.assertEqual(self.recipe.get_formatted_ingredients(),
                         "<ul><li class='ingredientItem'>8 oz milk</li><li class='ingredientItem'>1 cup Lucky Charms</li></ul>")

    def test_get_instructions_list(self):
        self.assertEqual(self.recipe.get_instructions_list(), ["pour milk", "warm it up if needed", "pour cereal in"])

    def test_get_formatted_instructions(self):
        self.assertEqual(self.recipe.get_formatted_instructions(),
                         "<ol><li class='instructionItem'>pour milk</li><li class='instructionItem'>warm it up if needed</li><li class='instructionItem'>pour cereal in</li></ol>")

    def test_get_tag_list(self):
        self.assertEqual(self.recipe.get_tag_list(), ['Quick and Easy', 'Vegetarian'])

    def test_get_formatted_tags(self):
        self.assertEqual(self.recipe.get_formatted_tags(), '"Quick and Easy","Vegetarian"')

    def test_convert_mins_to_hhmm(self):
        self.assertEqual(self.recipe.convert_mins_to_hhmm(90), "1:30")
        self.assertNotEquals(self.recipe.convert_mins_to_hhmm(65), "1:5")

    def test_combine_times(self):
        self.assertEqual(self.recipe.combine_times(), "0:06")
        self.assertNotEquals(self.recipe.combine_times(), "0:6")

    # Database operations from here down
    def test_no_title(self):
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                ingredients = "1,,food",
                instructions = "cook",
                prepMinutes = 60,
                cookMinutes = 30,
                servings = 2
            )
            recipe.full_clean()

    def test_no_ingredients(self):
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                title = "my recipe",
                instructions = "cook",
                prepMinutes = 60,
                cookMinutes = 30,
                servings = 2
            )
            recipe.full_clean()

    def test_no_instructions(self):
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                title = "my recipe",
                ingredients = "1,,food",
                prepMinutes = 60,
                cookMinutes = 30,
                servings = 2
            )
            recipe.full_clean()

    def test_no_prepMinutes(self):
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                title = "my recipe",
                ingredients = "1,,food",
                instructions = "cook",
                cookMinutes = 30,
                servings = 2
            )
            recipe.full_clean()

    def test_no_cookMinutes(self):
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                title = "my recipe",
                ingredients = "1,,food",
                instructions = "cook",
                prepMinutes = 60,
                servings = 2
            )
            recipe.full_clean()

    def test_no_servings(self):
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                title = "my recipe",
                ingredients = "1,,food",
                instructions = "cook",
                prepMinutes = 60,
                cookMinutes = 30
            )
            recipe.full_clean()

    def test_add_recipe(self):
        recipe = {
            "title" : "my recipe",
            "ingredients" : "1,,food",
            "instructions" : "cook",
            "prepMinutes" : 60,
            "cookMinutes" : 30,
            "servings" : 2,
            "tags" : ['Tag 1', 'Tag 2']
        }
        id = crud_add_recipe(recipe)
        saved_recipe = Recipe.objects.get(pk=id)
        self.assertEqual(saved_recipe.title, "my recipe")
        self.assertEqual(saved_recipe.ingredients, "1,,food")
        self.assertEqual(saved_recipe.instructions, "cook")
        self.assertEqual(saved_recipe.prepMinutes, 60)
        self.assertEqual(saved_recipe.cookMinutes, 30)
        self.assertEqual(saved_recipe.servings, 2)
        self.assertEqual(saved_recipe.get_tag_list(), ["Tag 1", "Tag 2"])

    def test_edit_recipe(self):
        recipe = {
            "title" : "my recipe",
            "ingredients" : "1,,food",
            "instructions" : "cook",
            "prepMinutes" : 60,
            "cookMinutes" : 30,
            "servings" : 2,
            "tags" : ['Tag 1', 'Tag 2']
        }
        id = crud_add_recipe(recipe)
        saved_recipe = Recipe.objects.get(pk=id)
        self.assertEqual(saved_recipe.title, "my recipe")
        self.assertEqual(saved_recipe.ingredients, "1,,food")
        self.assertEqual(saved_recipe.instructions, "cook")
        self.assertEqual(saved_recipe.prepMinutes, 60)
        self.assertEqual(saved_recipe.cookMinutes, 30)
        self.assertEqual(saved_recipe.servings, 2)
        self.assertEqual(saved_recipe.get_tag_list(), ["Tag 1", "Tag 2"])

        edited_recipe = {
            "title" : "my edited recipe",
            "ingredients" : "2,,food",
            "instructions" : "chill",
            "prepMinutes" : 45,
            "cookMinutes" : 0,
            "servings" : 2,
            "tags" : ['Tag 1', 'Tag 2', 'Tag 3']
        }
        crud_edit_recipe(id, edited_recipe) # 1 Refers to previous test
        saved_recipe = Recipe.objects.get(pk=id)
        self.assertEqual(saved_recipe.title, "my edited recipe")
        self.assertEqual(saved_recipe.ingredients, "2,,food")
        self.assertEqual(saved_recipe.instructions, "chill")
        self.assertEqual(saved_recipe.prepMinutes, 45)
        self.assertEqual(saved_recipe.cookMinutes, 0)
        self.assertEqual(saved_recipe.servings, 2)
        self.assertEqual(saved_recipe.get_tag_list(), ["Tag 1", "Tag 2", "Tag 3"])

    def test_get_all_recipes(self):
        all_recipes = Recipe.objects.all()
        crud_all_recipes = crud_get_recipes()
        self.assertEqual(len(all_recipes), len(crud_all_recipes))
        for i in range(len(all_recipes)):
            self.assertEqual(all_recipes[i].title, crud_all_recipes[i].title)
            self.assertEqual(all_recipes[i].ingredients, crud_all_recipes[i].ingredients)
            self.assertEqual(all_recipes[i].instructions, crud_all_recipes[i].instructions)
            self.assertEqual(all_recipes[i].prepMinutes, crud_all_recipes[i].prepMinutes)
            self.assertEqual(all_recipes[i].cookMinutes, crud_all_recipes[i].cookMinutes)
            self.assertEqual(all_recipes[i].servings, crud_all_recipes[i].servings)
            self.assertEqual(all_recipes[i].tags, crud_all_recipes[i].tags)

    def test_get_one_recipe(self):
        recipe = {
            "title" : "my recipe",
            "ingredients" : "1,,food",
            "instructions" : "cook",
            "prepMinutes" : 60,
            "cookMinutes" : 30,
            "servings" : 2,
            "tags" : ['Tag 1', 'Tag 2']
        }
        id = crud_add_recipe(recipe)
        saved_recipe = crud_get_recipes(id = id) # Note slight difference from above
        self.assertEqual(saved_recipe.title, "my recipe")
        self.assertEqual(saved_recipe.ingredients, "1,,food")
        self.assertEqual(saved_recipe.instructions, "cook")
        self.assertEqual(saved_recipe.prepMinutes, 60)
        self.assertEqual(saved_recipe.cookMinutes, 30)
        self.assertEqual(saved_recipe.servings, 2)
        self.assertEqual(saved_recipe.get_tag_list(), ["Tag 1", "Tag 2"])

    def test_get_filtered_recipes_tags(self):
        recipes = [
            {
                "title" : "my recipe",
                "ingredients" : "1,,food",
                "instructions" : "cook",
                "prepMinutes" : 60,
                "cookMinutes" : 30,
                "servings" : 2,
                "tags" : ['Tag 1', 'Tag 2']
            },
            {
                "title" : "my second recipe",
                "ingredients" : "2,,food",
                "instructions" : "chill",
                "prepMinutes" : 45,
                "cookMinutes" : 0,
                "servings" : 2,
                "tags" : ['Tag 2', 'Tag 3']

            },
            {
                "title" : "another one",
                "ingredients" : "3,,food",
                "instructions" : "chill",
                "prepMinutes" : 45,
                "cookMinutes" : 0,
                "servings" : 2,
                "tags" : ['Tag 3', 'Tag 4']
            }
        ]
        ids = [crud_add_recipe(recipe) for recipe in recipes]

        # Contain Tag 1
        self.assertEqual([ids[0]], [recipe.id for recipe in crud_get_recipes(tags = ["Tag 1"])])

        # Contain Tag 2
        self.assertEqual([ids[0], ids[1]], [recipe.id for recipe in crud_get_recipes(tags=["Tag 2"])])

        # Contain Tag 3
        self.assertEqual([ids[1], ids[2]], [recipe.id for recipe in crud_get_recipes(tags=["Tag 3"])])

        # Contain Tag 4
        self.assertEqual([ids[2]], [recipe.id for recipe in crud_get_recipes(tags=["Tag 4"])])

    def test_get_filtered_recipes_query(self):
        recipes = [
            {
                "title" : "my recipe",
                "ingredients" : "1,,food",
                "instructions" : "cook",
                "prepMinutes" : 60,
                "cookMinutes" : 30,
                "servings" : 2,
                "tags" : ['Tag 1', 'Tag 2']
            },
            {
                "title" : "my second recipe",
                "ingredients" : "2,,food",
                "instructions" : "chill",
                "prepMinutes" : 45,
                "cookMinutes" : 0,
                "servings" : 2,
                "tags" : ['Tag 2', 'Tag 3']

            },
            {
                "title" : "another one",
                "ingredients" : "3,,food",
                "instructions" : "chill",
                "prepMinutes" : 45,
                "cookMinutes" : 0,
                "servings" : 2,
                "tags" : ['Tag 3', 'Tag 4']
            }
        ]
        ids = [crud_add_recipe(recipe) for recipe in recipes]

        # Contains "recipe"
        self.assertEqual([ids[0], ids[1]], [recipe.id for recipe in crud_get_recipes(query="recipe")])

        # Contains "RECIPE"
        self.assertEqual([ids[0], ids[1]], [recipe.id for recipe in crud_get_recipes(query="RECIPE")])

        # Contains the letter "n"
        self.assertEqual([ids[1], ids[2]], [recipe.id for recipe in crud_get_recipes(query="n")])

        # Contains the  word "Another"
        self.assertEqual([ids[2]], [recipe.id for recipe in crud_get_recipes(query="Another")])

    def test_delete_recipe(self):
        recipe = {
            "title": "my recipe",
            "ingredients": "1,,food",
            "instructions": "cook",
            "prepMinutes": 60,
            "cookMinutes": 30,
            "servings": 2,
            "tags": ['Tag 1', 'Tag 2']
        }
        id = crud_add_recipe(recipe)
        crud_get_recipes(id = id)
        crud_delete_recipe(id = id)
        self.assertRaises(IndexError, crud_get_recipes, id = id)

    # Test basic HTMl returns
    def test_addRecipe_view(self):
        response = self.client.get(reverse("addRecipe"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addRecipe.html')

    def test_editRecipe_view(self):
        response = self.client.get(reverse("editRecipe", kwargs={"prev_id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addRecipe.html')

    def test_viewRecipe_view(self):
        response = self.client.get(reverse("viewRecipe", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewRecipe.html')

    def test_index_view(self):
        response = self.client.get(reverse("browseRecipe"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browseRecipes.html')

    def test_deleteRecipe_view(self):
        response = self.client.get(reverse("deleteRecipe", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browseRecipes.html')

    def test_browseRecipes_view(self):
        response = self.client.get(reverse("browseRecipe2"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browseRecipes.html')

    def test_missing_image_info(self):
        recipe = {
            "title": "my recipe",
            "ingredients": "1,,food",
            "instructions": "cook",
            "prepMinutes": 60,
            "cookMinutes": 30,
            "servings": 2,
            "tags": ['Tag 1', 'Tag 2'],
        }
        self.assertEqual(recipe, process_image_dict(recipe, recipe))

    def test_remove_image_info(self):
        form_entry = {
            "title": "my recipe",
            "ingredients": "1,,food",
            "instructions": "cook",
            "prepMinutes": 60,
            "cookMinutes": 30,
            "servings": 2,
            "tags": ['Tag 1', 'Tag 2'],
            "image": 1,
            "maintain-image": "Delete Image"
        }
        recipe = {
            "title": "my recipe",
            "ingredients": "1,,food",
            "instructions": "cook",
            "prepMinutes": 60,
            "cookMinutes": 30,
            "servings": 2,
            "tags": ['Tag 1', 'Tag 2'],
            "image": 5
        }
        self.assertEqual(recipe.items(), process_image_dict(form_entry, recipe).items())

    def test_keep_image_info(self):
        form_entry = {
            "title": "my recipe",
            "ingredients": "1,,food",
            "instructions": "cook",
            "prepMinutes": 60,
            "cookMinutes": 30,
            "servings": 2,
            "tags": ['Tag 1', 'Tag 2'],
            "image": 1,
            "maintain-image": "Keep Image"
        }
        recipe = {
            "title": "my recipe",
            "ingredients": "1,,food",
            "instructions": "cook",
            "prepMinutes": 60,
            "cookMinutes": 30,
            "servings": 2,
            "tags": ['Tag 1', 'Tag 2'],
            "image": 5
        }
        modified_recipe = {
            "title": "my recipe",
            "ingredients": "1,,food",
            "instructions": "cook",
            "prepMinutes": 60,
            "cookMinutes": 30,
            "servings": 2,
            "tags": ['Tag 1', 'Tag 2'],
        }
        self.assertEqual(modified_recipe.items(), process_image_dict(form_entry, recipe).items())

    def test_add_image(self):
        temp_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        recipe = {
            "title" : "my recipe",
            "ingredients" : "1,,food",
            "instructions" : "cook",
            "prepMinutes" : 60,
            "cookMinutes" : 30,
            "servings" : 2,
            "tags" : ['Tag 1', 'Tag 2'],
            "image" : temp_image
        }
        id = crud_add_recipe(recipe)
        recipe_with_image = crud_get_recipes(id = id)
        self.assertEqual(recipe_with_image.image.url, "/media" + temp_image)

    def test_remove_image(self):
        temp_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        recipe = {
            "title" : "my recipe",
            "ingredients" : "1,,food",
            "instructions" : "cook",
            "prepMinutes" : 60,
            "cookMinutes" : 30,
            "servings" : 2,
            "tags" : ['Tag 1', 'Tag 2'],
            "image" : temp_image,
        }
        id = crud_add_recipe(recipe)
        recipe_with_image = crud_get_recipes(id = id)

        remove_image_form = recipe
        remove_image_form["maintain-image"] = "Remove Image"
        remove_image_form["image"] = None
        recipe = process_image_dict(remove_image_form, recipe)

        crud_edit_recipe(id, recipe)
        recipe_without_image = crud_get_recipes(id=id)

        # Checks if there is no image, this is because it returns a
        # special "None"
        self.assertEqual(bool(recipe_without_image.image), False)