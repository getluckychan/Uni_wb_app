from django import forms
from vnz.models import *


# class SearchUserForm(forms.ModelForm):
#     class Meta:
#         model = MyUser
#         fields = ('full_name',)
#         widgets = {
#             'full_name': forms.ModelChoiceField(queryset=MyUser.objects.all().only('full_name').order_by('full_name'))
#         }
