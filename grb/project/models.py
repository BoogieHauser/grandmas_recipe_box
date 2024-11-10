from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    prepMinutes = models.IntegerField()
    cookMinutes = models.IntegerField()
    servings = models.IntegerField()

    def getIngredients(self):
        html = []
        html.append("<ul>")
        lines = self.ingredients.split("\n")
        for line in lines:
            html.append("<li>" + line + "</li>")
        html.append("</ul>")
        return "".join(html)


