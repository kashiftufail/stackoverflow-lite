# questions/forms.py
from django import forms
from .models import Question
from django_select2.forms import Select2TagWidget   # the only widget we need

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "detail", "tags"]
        widgets = {
            "title":  forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "detail": forms.Textarea(attrs={"class": "w-full p-2 border rounded"}),
            # Select2 sends Ajax to our autocomplete URL and lets users add new tags
            "tags": Select2TagWidget(
                attrs={
                    "class": "w-full",
                    "data-tags": "true",                # allow new tags
                    "data-ajax--url": "/autocomplete/tags/",
                    "data-placeholder": "Add tags…",
                    "data-minimum-input-length": "1",
                }
            ),
        }

    def clean_tags(self):
        """
        Clean and split incoming tags. Handles:
        - Raw list (from Select2)
        - Stringified list (Select2 may send: '["a", "b"]')
        - Quoted tags like "'oracle'" or "['foo']"
        """
        tags = self.cleaned_data["tags"]

        # Handle single comma-separated string
        if isinstance(tags, str):
            tags = tags.split(",")

        cleaned = []
        for tag in tags:
            tag = tag.strip().strip("[]'\"")  # remove quotes, brackets, spaces
            if tag:
                cleaned.append(tag)
        print("Cleaned tags:", cleaned)
        return cleaned
    
