from django import forms
from .models import Comment


class SearchForm(forms.Form):
    """Search form."""
    query = forms.CharField(max_length=100,
                            label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Just type ship or country...',
                                                          'class': 'form-control form-control-lg'}))


class ContactForm(forms.Form):
    """Base contact form class."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    subject = forms.CharField(required=True, max_length=200)
    message = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        """
        Added 'placeholder' attribute by customizing the default widget and
        form control class for all fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['subject'].widget.attrs.update({'placeholder': 'Subject'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Enter your message here.'})
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
