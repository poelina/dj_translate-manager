from django import forms

def validate_special_character(value):
    special_characters = "!@#$%^&*()-_=+[{]};:'\,<.>/?\|`~"
    has_char = False
    for char in value:
        if char in special_characters:
            has_char = True
            break
    if not has_char:
        raise forms.ValidationError("Must contain at least one special symbol.")

class UserForm(forms.Form):
    user_email = forms.EmailField(
        label = "Email:",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'}),
        min_length=6,
        max_length=50,
    )
    user_password = forms.CharField(
        label = "Password:",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'}),
        min_length=5,
        max_length=20,
    )

class RegisterForm(forms.Form):
    user_name = forms.CharField(
        label = "Your Name:",
        widget = forms.TextInput(attrs={'placeholder': 'Enter Your Name'}),
        min_length=3,
        max_length=20,
    )
    user_surname = forms.CharField(
        label = "Your Surname:",
        widget = forms.TextInput(attrs={'placeholder': 'Enter Your Surname'}),
        min_length=3,
        max_length=20,
    )
    user_email = forms.EmailField(
        label = "Email:",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'}),
        min_length=6,
        max_length=50,
    )

    user_password = forms.CharField(
        label = "Password:",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'}),
        min_length=5,
        max_length=20,
        validators=[validate_special_character],
    )