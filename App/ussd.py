from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from africastalking.utils import sanitize_phone_number
from .models import ReportedPhoneNumber
from .forms import AddPhoneNumberForm

@csrf_exempt
@require_POST
def ussd_callback(request):
    # Parse the USSD request
    service_code = request.POST.get('serviceCode', '')
    phone_number = request.POST.get('phoneNumber', '')
    session_id = request.POST.get('sessionId', '')
    text = request.POST.get('text', '').strip()

    # Handle the USSD request
    if text == '':
        # Main menu
        response_text = '1. Add a fraudulent phone number\n2. Search for a phone number'
        response = 'CON %s' % response_text
    elif text == '1':
        # Add a fraudulent phone number
        response_text = 'Enter the phone number in international format (e.g. +254712345678)'
        response = 'CON %s' % response_text
    elif text.startswith('1*'):
        # Save the fraudulent phone number
        phone_number = text.split('*')[-1]
        form = AddPhoneNumberForm({'phone_number': phone_number})
        if form.is_valid():
            reported_phone_number, created = ReportedPhoneNumber.objects.get_or_create(phone_number=phone_number)
            if created:
                reported_phone_number.report_count = 1
                reported_phone_number.save()
            else:
                if reported_phone_number.reported_by.filter(id=request.user.id).exists():
                    # User has already reported this phone number
                    response_text = 'You have already reported this phone number.'
                    response = 'CON %s' % response_text
                    return HttpResponse(response)
                else:
                    reported_phone_number.report_count += 1
                    reported_phone_number.reported_by.add(request.user)
                    reported_phone_number.save()
            response_text = 'The phone number %s has been added to the database.' % phone_number
            response = 'END %s' % response_text
        else:
            response_text = 'Invalid input. Please enter the phone number in international format (e.g. +254712345678)'
            response = 'CON %s' % response_text
    elif text == '2':
        # Search for a phone number
        response_text = 'Enter the phone number in international format (e.g. +254712345678)'
        response = 'CON %s' % response_text
    elif text.startswith('2*'):
        # Lookup the phone number
        phone_number = text.split('*')[-1]
        queryset = ReportedPhoneNumber.objects.filter(phone_number=phone_number)
        if queryset.exists():
            report_count = queryset.first().report_count
            response_text = 'The phone number %s has been reported %d times.' % (phone_number, report_count)
            response = 'END %s' % response_text
        else:
            response_text
