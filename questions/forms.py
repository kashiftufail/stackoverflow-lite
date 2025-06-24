from django import forms
from .models import Question
from taggit.forms import TagWidget

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'detail', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags'}),
        }