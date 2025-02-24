from django import forms
from django.core import validators

class ProductForm(forms.Form):
    name = forms.CharField(max_length = 100)
    price = forms.DecimalField(min_value=1, max_value=100000, decimal_places=2)
    description = forms.CharField(
        label="Product description",
        widget=forms.Textarea(attrs={"rows": 5, "cols": 10}),
        validators=[validators.RegexValidator(
            regex='great',
            message='Product must contain word "great"',
        )],
    )