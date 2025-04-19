from django import forms
from .models import Prompt

class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ['title', 'prompt_text', 'category', 'tags']