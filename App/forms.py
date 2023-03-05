from django import forms
from .models import ReportedPhoneNumber

class PhoneNumberSearchForm(forms.Form):
    phone_number = forms.CharField(max_length=20)

class AddPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=20)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if ReportedPhoneNumber.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number has already been reported.")
        return phone_number

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)