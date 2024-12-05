from django.db import models
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

class Recipe(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    ingredients = models.TextField(null=False, blank=False)
    instructions = models.TextField(null=False, blank=False)
    prepMinutes = models.IntegerField(null=False, blank=False)
    cookMinutes = models.IntegerField(null=False, blank=False)
    servings = models.IntegerField(null=False, blank=False)
    tags = TaggableManager()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail = ImageSpecField(
        source = 'image',
        processors = [ResizeToFit(300, 300)],
        format = 'JPEG',
        options = {'quality':80}
    )

    def get_ingredients_list(self):
        return self.ingredients.split("\n")

    def get_formatted_ingredients(self):
        html = []
        html.append("<ul>")
        lines = self.get_ingredients_list()
        for line in lines:
            html.append("<li class='ingredientItem'>" + self.clean_line(line) + "</li>")
        html.append("</ul>")
        return "".join(html)

    def get_instructions_list(self):
        return self.instructions.split('\n')

    def get_formatted_instructions(self):
        html = []
        html.append("<ol>")
        lines = self.get_instructions_list()
        for line in lines:
            html.append("<li class='instructionItem'>" + line + "</li>")
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

    def get_tag_list(self):
        return list(self.tags.names())

    def get_formatted_tags(self):
        return ','.join(['"{tag}"'.format(tag = tag) for tag in self.get_tag_list()])



