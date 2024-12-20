from django import forms
from .models import Record

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['id', 'name', 'title', 'content', 'classification', 'is_finance', 'tag']