from django import forms
from.models import *

class UpdateQuantityForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField()