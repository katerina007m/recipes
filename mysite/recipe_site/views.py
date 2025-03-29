from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from mysite.settings import BASE_DIR
from .forms import RecipeForm, RecipeFormEdit
from .models import Recipe, Category


# Главная страница
def home(request):
    recipes = Recipe.objects.all()

    if request.headers.get("Accept") == "application/json":
        return get_json_response(
            recipes=list(recipes), response_code=200, list_response=False
        )

    return render(
        request,
        BASE_DIR / "recipe_site/templates/home.html",
        {"recipes": recipes},
    )


# Подробности рецепта
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.headers.get("Accept") == "application/json":
        return get_json_response(recipes=(recipe,), response_code=200)

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

            if recipe.image.closed:
                recipe.image = form.files["file"]

            recipe.save()
            form.save_m2m()  # To save ManyToMany relations

            if request.headers.get("Accept") == "application/json":
                return get_json_response(
                    recipes=(recipe,),
                    message="Recipe successfully created",
                    response_code=201,
                )
            return redirect("recipe_detail", pk=recipe.pk)
        else:
            if request.headers.get("Accept") == "application/json":
                return get_json_response(
                    (), message="Invalid data submitted", response_code=400
                )
    else:
        form = RecipeForm()
        if request.headers.get("Accept") == "application/json":
            return get_json_response((), response_code=200)
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

            if request.headers.get("Accept") == "application/json":
                return get_json_response(
                    recipes=(recipe,),
                    message="Recipe successfully updated",
                    response_code=200,
                )

            return redirect("recipe_detail", pk=recipe.pk)

    else:
        form = RecipeForm(instance=recipe)

        if request.headers.get("Accept") == "application/json":
            return get_json_response(recipes=(recipe,), response_code=200)

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

    if request.headers.get("Accept") == "application/json":
        return get_json_response(
            recipes=(recipe,), message="Recipe successfully deleted", response_code=204
        )

    return redirect("home")


def get_json_response(recipes, message="", response_code=200, list_response=False):
    if len(recipes) == 0:
        return JsonResponse({"recipes": []}, status=response_code)

    data = []
    for recipe in recipes:
        data.append(
            {
                "id": recipe.pk,
                "name": recipe.name,
                "author": recipe.author.username,
                "created_at": recipe.created_at.isoformat(),
                "updated_at": recipe.updated_at.isoformat(),
                "description": recipe.description,
                "steps": recipe.steps,
                "cook_time": recipe.cook_time,
                "image": recipe.image.url.split("/")[-1] if recipe.image else None,
            }
        )
    if len(data) == 1:
        if not list_response:
            data = data[0]
        return JsonResponse({"recipe": data, "message": message}, status=response_code)
    return JsonResponse({"recipes": data, "message": message}, status=response_code)


@login_required
def api_get_recipe_pk_by_name(request, name):
    return _get_object_pk_by_name(request, Recipe, name)


@login_required
def api_get_category_pk_by_name(request, name):
    return _get_object_pk_by_name(request, Category, name)


def _get_object_pk_by_name(request, model, name):
    if not request.user.is_superuser:
        return JsonResponse({"id": 0}, status=403)

    if request.headers.get("Accept") != "application/json":
        return JsonResponse({"id": 0}, status=400)

    try:
        obj = model.objects.get(name=name)
    except model.DoesNotExist:
        return JsonResponse({"id": 0}, status=404)

    return JsonResponse({"id": obj.pk}, status=200)
