from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import GameProgress


class GameProgressForm(forms.ModelForm):
    class Meta:
        model = GameProgress
        fields = ['game', 'progress_note', 'hours_played']
        widgets = {
            'progress_note': forms.Textarea(attrs={'rows': 3}),
        }

