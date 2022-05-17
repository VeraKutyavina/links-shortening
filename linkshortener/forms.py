from django import forms

from .models import Link


# Main form for create short link with validation

class LinkShorterForm(forms.Form):
    long_link = forms.URLField(required=True, max_length=100, widget=forms.URLInput(
        attrs={"class": "input", "placeholder": "Write your URL here"}))

    class Meta:
        model = Link
        fields = 'long_link,'

