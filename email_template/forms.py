from django import forms


class CreatePDFTemplate(forms.Form):
    email = forms.EmailField()
