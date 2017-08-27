from django import forms


class SearchForm(forms.Form):
    """Search form."""
    query = forms.CharField(max_length=100,
                            label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Search'}))

