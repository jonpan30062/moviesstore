from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'movie_name']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter petition title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why this movie should be added to the store'
            }),
            'movie_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the movie name'
            })
        }
        labels = {
            'title': 'Petition Title',
            'description': 'Description',
            'movie_name': 'Movie Name'
        }
