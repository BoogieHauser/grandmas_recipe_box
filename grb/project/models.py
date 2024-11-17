from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    ingredients = models.TextField(null=False, blank=False)
    instructions = models.TextField(null=False, blank=False)
    prepMinutes = models.IntegerField(null=False, blank=False)
    cookMinutes = models.IntegerField(null=False, blank=False)
    servings = models.IntegerField(null=False, blank=False)

    def getIngredients(self):
        html = []
        html.append("<ul>")
        lines = self.ingredients.split("\n")
        for line in lines:
            html.append("<li>" + self.clean_line(line) + "</li>")
        html.append("</ul>")
        return "".join(html)

    def getInstructions(self):
        html = []
        html.append("<ol>")
        lines = self.instructions.split("\n")
        for line in lines:
            html.append("<li>" + line + "</li>")
        html.append("</ol>")
        return "".join(html)

    def convert_mins_to_hhmm(self, mins):
        hours = mins // 60
        minutes = mins % 60
        return f"{hours}:{minutes:02d}"

    def combine_times(self):
        total_time = self.prepMinutes + self.cookMinutes
        return self.convert_mins_to_hhmm(total_time)

    def clean_line(self, line):
        sep_line = line.split(",")
        clean_line = " ".join(sep_line)
        return clean_line





