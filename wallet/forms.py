from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(label='Ethereum Wallet Address', max_length=42)