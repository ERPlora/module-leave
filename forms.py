from django import forms
from django.utils.translation import gettext_lazy as _

from .models import LeaveType

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name', 'days_per_year', 'is_paid', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'days_per_year': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

