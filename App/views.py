from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import ReportedPhoneNumber
from .forms import PhoneNumberSearchForm, AddPhoneNumberForm, ContactForm
from django.views import View


class FraudulentPhoneNumbersView(TemplateView):
    template_name = 'app/fraudulent_phone_numbers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reported_phone_numbers = ReportedPhoneNumber.objects.all()

        for reported_phone_number in reported_phone_numbers:
            reported_phone_number.report_count = reported_phone_number.reports.count()



        context['reported_phone_numbers'] = reported_phone_numbers

        return context



class PhoneNumberSearchView(TemplateView):
    template_name = 'app/phone_number_search.html'

    def get(self, request, *args, **kwargs):
        form = PhoneNumberSearchForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PhoneNumberSearchForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            queryset = ReportedPhoneNumber.objects.filter(phone_number__icontains=phone_number)
            context = {'form': form, 'queryset': queryset}
            return render(request, self.template_name, context)
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


class AddPhoneNumberView(View):
    template_name = 'app/add_fraudulent_phone_numbers.html'

    def get(self, request):
        form = AddPhoneNumberForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = AddPhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            reported_phone_number, created = ReportedPhoneNumber.objects.get_or_create(phone_number=phone_number)
            if created:
                reported_phone_number.report_count = 1
                reported_phone_number.save()
            else:
                if reported_phone_number.reported_by.filter(id=request.user.id).exists():
                    # User has already reported this phone number
                    form.add_error('phone_number', 'You have already reported this phone number.')
                    context = {'form': form}
                    return render(request, self.template_name, context)
                else:
                    reported_phone_number.report_count += 1
                    reported_phone_number.reported_by.add(request.user)
                    reported_phone_number.save()
            return redirect('fraudulent_phone_numbers')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

class ContactUs(TemplateView):
    template_name = 'app/contact_us.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email logic here
            return render(request, self.template_name, {'success': True})
        else:
            context = {'form': form}
            return render(request, self.template_name, context)