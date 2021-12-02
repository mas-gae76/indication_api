from django import forms
from .models import Counter, History
from django.shortcuts import get_object_or_404, get_list_or_404


class CounterAdminForm(forms.ModelForm):

    class Meta:
        model = Counter
        fields = ('name', 'user', 'value', )

    def clean(self):
        cd = self.cleaned_data
        cur_value = cd.get('value')
        prev_value = self.instance.value
        if cur_value < prev_value:
            raise forms.ValidationError('Показание меньше переданного ранее!')
        return cd
