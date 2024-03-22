from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Column, Field, Row, Submit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Row(Column(Field("username", autofocus=True))),
            Row(Column("password")),
            Submit("submit", "Submit", css_class="btn btn-secondary btn-lg w-100"),
        )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Row(Column(Field("username", autofocus=True))),
            Row(Column("first_name")),
            Row(Column("last_name")),
            Row(Column("email")),
            Row(Column("password1")),
            Row(Column("password2")),
            Submit("submit", "Submit", css_class="btn btn-secondary btn-lg w-100"),
        )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
