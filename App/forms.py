from django import forms
from .models import ReportedPhoneNumber

class PhoneNumberSearchForm(forms.Form):
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Format 712345678 or 112345678'}))

    def cleaned_phone_number(self):
        phone_number = self.clean_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError('Enter a valid phone number')
        if not ReportedPhoneNumber.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Number not found')
        return phone_number


class AddPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(min_length=9,max_length=9, widget=forms.TextInput(attrs={'placeholder': 'Format 712345678 or 112345678'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not isinstance(phone_number, int):
            raise forms.ValidationError('Enter a valid phone number')
        if ReportedPhoneNumber.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number has already been reported.")
        return phone_number


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)