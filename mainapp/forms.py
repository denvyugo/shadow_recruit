from django import forms
from .models import Recruit


class RecruitCreateForm(forms.ModelForm):
    """form for recruit profile"""
    class Meta:
        model = Recruit
        exclude = ('master',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
