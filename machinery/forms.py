from django import forms

class ItemsForm(forms.Form):
    category_id = forms.IntegerField()
    user_id = forms.IntegerField()
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Write your name here'
            }
        )
    )
    description = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'description'
            }
        )
    )
    price_for_lease = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Location'
            }
        )
    )
    location = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Location'
            }
        )
    )
    pictures = forms.ImageField()