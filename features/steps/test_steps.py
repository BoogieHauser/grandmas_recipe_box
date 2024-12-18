from django.urls import reverse
from recipes.models import Recipe
from behave import given, when, then
from django.test.client import Client
from django.contrib.auth.models import User

@given('there are recipes in the database')
def step_impl(context):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword'
    )

    recipe = Recipe.objects.create(
        title="Breakfast Cereal",
        ingredients="""8,oz,milk
    1,cup,Lucky Charms""",
        instructions="""pour milk
    warm it up if needed
    pour cereal in""",
        prepMinutes=5,
        cookMinutes=1,
        servings=1,
        user=user,
    )
    recipe.tags.add("Quick and Easy", "Vegetarian")

@when('I visit the browse recipes page')
def step_impl(context):
    client = Client()
    client.login(username='testuser', password='testpassword')
    context.response = client.get(reverse('browseRecipe'))

@then('I should see a list of recipes')
def step_impl(context):
    assert "Breakfast Cereal" in context.response.content.decode()