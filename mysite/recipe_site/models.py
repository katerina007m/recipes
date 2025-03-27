from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название рецепта")
    description = models.TextField(verbose_name="Описание")
    steps = models.TextField(verbose_name="Шаги приготовления")
    cook_time = models.IntegerField(verbose_name="Время приготовления (в минутах)")
    image = models.ImageField(
        upload_to="recipes/", null=True, blank=True, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    categories = models.ManyToManyField(
        Category, through="RecipeCategory", verbose_name="Категории"
    )

    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )

    def __str__(self):
        return f"{self.recipe.name} - {self.category.name}"
