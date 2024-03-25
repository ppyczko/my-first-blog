from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Row, Column, Field, Button

from .models import Post, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Row(Column(Field("title", autofocus=True))),
            Row(Column("text")),
            Row(Column("category")),
            Submit("submit", "Save", css_class="btn btn-secondary btn-lg w-100"),
        )

    class Meta:
        model = Post
        fields = ("title", "text", "category")


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Comment here !",
                "rows": 3,
                "cols": 50,
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["body"]
