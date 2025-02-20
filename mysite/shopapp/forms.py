from django import forms

class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length = 100)
    price = forms.DecimalField(min_value=1, max_value=100000)
    description = forms.CharField(label="Prosuct description", widget=forms.Textarea)