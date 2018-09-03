from django import forms
from .models import Poll, Choice

class CariPollForm(forms.Form):
    cari = forms.CharField(widget=forms.TextInput(attrs={'type':'search', 'placeholder':'cari', 'name':'cari'}))

class AddPollForm(forms.Form):
    text = forms.CharField(label='Text', min_length=5)
    pilihan1 = forms.CharField()
    pilihan2 = forms.CharField()

    def clean_text(self):
        text = self.cleaned_data['text']
        qs = Poll.objects.filter(text__iexact=text)
        if qs.exists():
            raise forms.ValidationError('Polling sudah pernah dibuat !')
        return text

class EditPollForm(forms.ModelForm):
    class Meta :
        model = Poll
        fields = ['text']
        widgets = {
            'text': forms.Textarea()
        }

class AddChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

class EditChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']


#
