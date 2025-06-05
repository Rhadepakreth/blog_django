from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('contenu',)
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ajoutez votre commentaire...'}),
        }

from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})