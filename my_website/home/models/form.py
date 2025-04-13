# myapp/forms.py
from django import forms
from .comment import Comment  

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'score', 'image']

        image = forms.ImageField(required=False) 