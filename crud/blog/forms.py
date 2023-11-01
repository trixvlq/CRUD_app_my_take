from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(label='', widget=forms.Textarea(
        attrs={"label": "", "name": "text", "class": "form-control", "placeholder": "Add your comment", 'rows': 4}))

