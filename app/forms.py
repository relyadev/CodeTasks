from django import forms
from .models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}),
        label='Подтверждение пароля'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'password': 'Пароль',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        username = cleaned_data.get("username")

        unresolved_names = ["admin", ""]
        if username in unresolved_names:
            self.add_error("username", "Данное имя нельзя использовать")

        if len(username) < 5:
            self.add_error("username", "Имя должно содержать не менее 5 символов")

        if len(password) < 8:
            self.add_error('password', "Пароль должен содержать 8 и более символов")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают")


        return cleaned_data

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        is_exist = User.objects.filter(username=username).exists()

        if is_exist:
            self.add_error('username', "Такой username уже используется")
        return cleaned_data