from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from django.core.mail import mail_admins
from RealEstatePortal2.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import PropertyEnquiry




class PropertyEnquiryView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'property_enquiry.html', {})

    def post(self, request, *args, **kwargs):
        property_enquiry = PropertyEnquiry(
            client_name=request.POST['client_name'],
            email = request.POST['email'],
            phone_number = request.POST['phone_code'] + request.POST['phone_number'],
            property_ref = request.POST['property_ref'],
            comment = request.POST['comment'],
        )
        property_enquiry.save()

        # получаем наш html
        html_content = render_to_string(
            'emails/property_enquiry_submitted.html',
            {
                'property_enquiry': property_enquiry,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Property enquiry No {property_enquiry.id} by {property_enquiry.client_name} at QL Exiles',
            body=f'Dear Mr/Mrs {property_enquiry.client_name},\n\n\n'
                    f'Thank you for your request, your enquiry No {property_enquiry.id} has been submitted.\n'
                    f'Our agent will contact you within 24 hours.\n\n'
                    f'Your enquiry: {property_enquiry.comment}\n\n'
                    f'Kind Regards,\n'
                    f'Your QL Exiles Team',
            from_email=EMAIL_HOST_USER,
            to=[f'{property_enquiry.email}']
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        '''

        send_mail(
            subject=f'Property enquiry No {property_enquiry.id} by {property_enquiry.client_name} at QL Exiles',
            message=f'Dear Mr/Mrs {property_enquiry.client_name},\n\n\n'
                    f'Thank you for your request, your enquiry No {property_enquiry.id} has been submitted.\n'
                    f'Our agent will contact you within 24 hours.\n\n'
                    f'Your enquiry: {property_enquiry.comment}\n\n'
                    f'Kind Regards,\n'
                    f'Your QL Exiles Team',
            from_email=EMAIL_HOST_USER,
            recipient_list=[f'{property_enquiry.email}']
        )
        '''
        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        mail_admins(
            subject=f'Property enquiry No {property_enquiry.id} by {property_enquiry.client_name} at QL Exiles',
            message=f'Dear Admins Team,\n\n'
                    f'A new property enquiry No {property_enquiry.id} by Mr/Mrs {property_enquiry.client_name}:\n\n'
                    f'Property Ref No: {property_enquiry.property_ref}\n'
                    f'Submitted at: {property_enquiry.date_time}\n'
                    f'Enquiry text: {property_enquiry.comment}\n'
        )

        return redirect('contactus:property_enquiry')
