from django import forms
from django.core.exceptions import ValidationError

from core.models import Item, Tag

class ItemForm(forms.ModelForm):

    class Meta:

        TAGS_HELP_TEXT = "Tags are used to categorise items dynamically. You can create your own tags and categorise items with them as you see fit."

        model = Item

        fields = [
            "name",
            "description",
            "is_complete",
            "tags",
            "start_datetime",
            "end_datetime",
        ]

        help_texts = {
            "tags": TAGS_HELP_TEXT,
        }

        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
            "start_datetime": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={
                "type": "datetime-local",
            }),
            "end_datetime": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={
                "type": "datetime-local",
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        if self.user is None:
            raise ValueError("A user argument is required.")

        super().__init__(*args, **kwargs)

        self.fields["tags"].queryset = Tag.objects.filter(user=self.user)

class TagForm(forms.ModelForm):

    class Meta:

        model = Tag

        fields = [
            "name",
            "colour",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        if self.user is None:
            raise ValueError("A user argument is required.")

        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data["name"]

        pre_existing_user_tag = Tag.objects.filter(user=self.user, name=name).first()

        if not pre_existing_user_tag:
            return name

        is_other_tag = pre_existing_user_tag.id != self.instance.id

        if pre_existing_user_tag and is_other_tag:
            raise ValidationError("The tag name must be unique.")

        return name
