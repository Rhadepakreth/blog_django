from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('contenu',)
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ajoutez votre commentaire...'}),
        }