from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "<i class='fa-solid fa-envelope'></i>Email"
        self.fields["password"].label = "<i class='fa-solid fa-key'></i>Password"

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Sorry, that login was invalid. Please try again.")
        return super().clean()

    def userlogin(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        return user


class SignupForm(LoginForm):
    username = forms.CharField(
        label="Username",
        min_length=5,
        validators=[],
        widget=forms.TextInput(attrs={
            'placeholder': 'Type a name more than 5 letters',
            'hx-post': '/user/check_username/',
            'hx-trigger': 'keyup',
            'hx-target': '#username-avail'
        }))
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    field_order = ['username', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "<i class='fa-solid fa-user'></i>Username"
        self.fields["confirm_password"].label = "<i class='fa-solid fa-lock'></i>Confirm Password"

    def clean(self):
        username = str(self.cleaned_data.get('username')).replace(' ', '')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                f"Password didn't match for {username}")

        if User.objects.filter(email=email).first():
            raise forms.ValidationError(
                f"{email} already exists! Try logging instead")

        User.objects.create_user(
            email=email, username=username, password=password)

        return super().clean()
