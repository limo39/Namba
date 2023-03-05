from django.urls import path
from .views import FraudulentPhoneNumbersView, PhoneNumberSearchView, AddPhoneNumberView, ContactUs

urlpatterns = [
    path('', FraudulentPhoneNumbersView.as_view(), name='fraudulent_phone_numbers'),
    path('search/', PhoneNumberSearchView.as_view(), name='phone_number_search'),
    path('add/', AddPhoneNumberView.as_view(), name='add_phone_number'),
    path('contact_us/', ContactUs.as_view(), name='contact_us'),
]
