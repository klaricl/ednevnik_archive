from django import forms
from appmessages.models import ContactMessages

class ContactMessagesForm(forms.ModelForm):
    name = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.EmailField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    subject = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(label = False, widget=forms.Textarea(attrs={'placeholder': 'Type your message...'}))

    class Meta():
        model = ContactMessages
        fields = ('__all__')
