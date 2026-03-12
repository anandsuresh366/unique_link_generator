from django import forms

class LinkForm(forms.Form):

    original_url = forms.URLField(
        label="Original URL",
        widget=forms.URLInput(attrs={
            "placeholder": "https://example.com"
        })
    )

    device_limit = forms.IntegerField(
        label="Device Limit",
        min_value=1,
        widget=forms.NumberInput(attrs={
            "placeholder": "Enter device limit"
        })
    )