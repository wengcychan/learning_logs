from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

"""A widget is an HTML form element, such as a single-line text box,
multiline text area, or drop-down list. By including the widgets attribute,
you can override Django's default widget choices. Here we tell Django to use 
a 'forms.Textarea' element with a width of 80 columns, instead of the 
default 40 columns. This gives users enough room to write a meaningful entry."""
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}