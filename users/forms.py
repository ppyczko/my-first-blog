from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Column, Field, Row, Submit
from django.contrib.auth.forms import AuthenticationForm


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
