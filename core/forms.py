from django import forms


class SearchForm(forms.Form):
    """Search form."""
    query = forms.CharField(max_length=100,
                            label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Just type ship or country...',
                                                          'class': 'form-control form-control-lg'}))

