from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "<i class='fa-solid fa-envelope'></i>Email"
        self.fields["password"].label = "<i class='fa-solid fa-key'></i>Password"

class SignupForm(LoginForm):
    username = forms.CharField(label="Username")
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    field_order = ['username','email','password','confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "<i class='fa-solid fa-user'></i>Username"
        self.fields["confirm_password"].label = "<i class='fa-solid fa-lock'></i>Confirm Password"

