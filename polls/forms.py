from django import forms

from .models import Poll, Choice


class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        exclude = ['author']


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        exclude = ['question']
