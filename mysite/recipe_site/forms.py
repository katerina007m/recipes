from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "steps", "cook_time", "image", "categories"]
        widgets = {
            "categories": forms.CheckboxSelectMultiple(),
        }


class RecipeFormEdit(RecipeForm):
    # For allowing partial update
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False  # Make all fields optional for partial updates
