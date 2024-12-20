from django import forms
from .models import Record

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['id', 'title', 'text', 'comment_id', 'grade', 'is_new', 'is_quailfied', 'feedback_type', 'is_finance', 'subcategory_type']
