from django import forms
from user_panel.models import SupportRequest

class SupportResponseForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
