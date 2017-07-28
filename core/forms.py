from django import forms


class SearchFrom(forms.Form):
    """Search form."""
    query = forms.CharField(max_length=100)

