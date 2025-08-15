from django import forms
from .models import Poll, Choice

'''class PollAddForm(forms.ModelForm):
    choice1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choice 1'}))
    choice2 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choice 2'}))

    class Meta:
        model = Poll
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Question text'}),
        }'''

class PollAddForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["text"]  # just the question text
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        
class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text', 'active']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
