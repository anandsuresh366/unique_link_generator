from django import forms

class LinkForm(forms.Form):
    original_url=forms.URLField()
    device_limit=forms.IntegerField(min_value=1)
