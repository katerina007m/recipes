import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from mysite.settings import BASE_DIR
from .forms import RecipeForm, RecipeFormEdit
from .models import Recipe


# Главная страница
def home(request):
    recipes = Recipe.objects.all()
    random_recipes = random.sample(list(recipes), min(5, len(recipes)))
    return render(
        request,
        BASE_DIR / "recipe_site/templates/home.html",
        {"recipes": random_recipes},
    )


# Подробности рецепта
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(
        request,
        BASE_DIR / "recipe_site/templates/recipe_detail.html",
        {"recipe": recipe},
    )


# Добавление рецепта
@login_required
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()  # Для сохранения связей ManyToMany
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(
        request, BASE_DIR / "recipe_site/templates/recipe_form.html", {"form": form}
    )


@login_required
def recipe_edit(request, pk):
    if (
        not request.user.is_superuser
        and request.user != Recipe.objects.get(pk=pk).author
    ):
        return redirect("home")

    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = RecipeFormEdit(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            form.save_m2m()

            return redirect("recipe_detail", pk=recipe.pk)

    else:
        form = RecipeForm(instance=recipe)

    return render(request, "recipe_form.html", {"form": form})


@login_required
def recipe_delete(request, pk):
    if (
        not request.user.is_superuser
        and request.user != Recipe.objects.get(pk=pk).author
    ):
        return redirect("home")

    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()

    return redirect("home")
