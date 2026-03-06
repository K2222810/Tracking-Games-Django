from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import GameProgress
from .models import Game
from django.forms import ModelForm, TextInput


class GameProgressForm(forms.ModelForm):
    class Meta:
        model = GameProgress
        fields = ['game', 'progress_note', 'hours_played']
        widgets = {
            'progress_note': forms.Textarea(attrs={'rows': 3}),
        }


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'platform', 'status', 'rank', 'price', 'release_date', 'purchase_date', 'cover_url', 'want_to_play_date']
        widgets = {
            'release_date': TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'autocomplete': 'off'}),
            'purchase_date': TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'autocomplete': 'off'}),
            'want_to_play_date': TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'autocomplete': 'off'}),
            'cover_url': TextInput(attrs={'placeholder': 'https://'}),
        }

