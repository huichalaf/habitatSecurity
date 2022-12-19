from django import forms
from .models import Users

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['user', 'password']
        widgets = {
        'user': forms.TextInput(attrs={'class': 'form-control'}),
        'password': forms.PasswordInput(),
    }