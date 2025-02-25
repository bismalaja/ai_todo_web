from django import forms
from .models import TodoItem

class TodoItenForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'description']