from django.test import TestCase
from .models import Recipe

class RecipeTest(TestCase):
    def setUp(self):
        self.recipe = Recipe(
            title = "Breakfast Cereal",
            ingredients = """8,oz,milk
1,cup,Lucky Charms""",
            instructions = """pour milk
warm it up if needed
pour cereal in""",
            prepMinutes = 5,
            cookMinutes = 1,
            servings = 1
        )

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


    def test_view_recipe(self):
        self.assertEqual(self.recipe.getIngredients(),
                         "<ul><li>8,oz,milk</li><li>1,cup,Lucky Charms</li></ul>")

# class RecipeModelTest(TestCase):
#     def setUp(self):
#
#

        # class RecipeModelTest(TestCase):
        #
        #     def setUp(self):
        #         # This method runs before each test
        #         self.recipe = Recipe.objects.create(
        #             title="Simple Pancakes",
        #             ingredients="Flour, Eggs, Milk, Sugar, Butter",
        #             instructions="Mix all ingredients. Cook on a hot pan.",
        #             cooking_time=10
        #         )
        #
        #     def test_recipe_creation(self):
        #         """Test that a Recipe instance is created correctly"""
        #         self.assertEqual(self.recipe.title, "Simple Pancakes")
        #         self.assertEqual(self.recipe.ingredients, "Flour, Eggs, Milk, Sugar, Butter")
        #         self.assertEqual(self.recipe.cooking_time, 10)
