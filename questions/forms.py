from django import forms
from questions.models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
