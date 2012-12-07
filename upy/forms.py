"""
Contains some form fields as utilities
"""
from django import forms
from upy.widgets import NullTrueCheckboxWidget

class NullTrueField(forms.NullBooleanField):
    """
    A field whose valid values are None and True. 
    """
    widget = NullTrueCheckboxWidget