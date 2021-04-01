from django import forms
from network.models import Post, User, Profile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, AuthenticationForm   

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    class Meta:
        model = Profile
        fields = ['title', 'dob', 'about', 'image']
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control form-control-sm', 'Placeholder': 'Title'}),
            'dob' : forms.DateInput(attrs={'class' : 'form-control form-control-sm', 'type': 'date'}),
            'about' : forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows' : '3'}),
            'image' : forms.FileInput(attrs={'class': ''})
        }
        help_texts = {
            'image' : "Choose A Profile Picture."
        }


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control form-control-sm', 'Placeholder': 'Username'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control form-control-sm', 'type': 'email'}),
        }
        help_texts = {
            'username' : ""
        }

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control form-control-sm"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control form-control-sm"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control form-control-sm"})

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, "class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', "class": "form-control", "placeholder": "Password"}),
    )
