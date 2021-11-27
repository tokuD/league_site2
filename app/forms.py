from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import DeckThema, Match, Skill, Result, UseDeck
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django import forms
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)

class UseDeckForm(ModelForm):
    class Meta:
        model = UseDeck
        fields = ['match', 'image1', 'image2']


class MatchForm(forms.Form):
    date = forms.DateTimeField(
        label='開始時刻',
        widget=forms.DateTimeInput(attrs={
            "type": "datetime-local",
            "value": timezone.datetime.now().strftime('%Y-%m-%dT%H:%M')
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    player2 = forms.ChoiceField(
        label='対戦相手',
        required=True,
    )


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = ['match', 'deck', 'skill', 'result1', 'result2', 'result3', 'comment']


class SearchForm(forms.Form):
    player = forms.CharField(max_length=20, required=False)
