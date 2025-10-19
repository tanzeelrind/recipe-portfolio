from django.db import models
from django.contrib.auth.models import *
class Recipe(models.Model):
    owner=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipe_name_from_models=models.CharField(max_length=100)
    recipe_description_from_models=models.TextField()
    recipe_image_from_models=models.ImageField(upload_to="cupboard")
    def __str__(self):
        return self.recipe_name_from_models
