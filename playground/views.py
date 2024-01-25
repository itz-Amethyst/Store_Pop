from django.core.mail import send_mail , mail_admins , BadHeaderError, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks.main import notify_customers


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def say_hello(request):
    try:
        # message = EmailMessage('subject', 'message', 'from@gmail.com', ['admin@gmail.com'])
        # message.attach_file('uploads/store/images/productId_1/peakpx_1.jpg')
        # message.send()
        #
        # # send_mail('subject', 'test message', 'info@gmail.com', '')
        # mail_admins('subject', 'message', html_message = '<h2>Hi</h2>')

        message = BaseEmailMessage (
            template_name = 'emails/hello.html',
            context = {'ip': get_client_ip(request)}
        )
        message.send(['info@admin.com'])
    except BadHeaderError:
        pass

    return render(request, 'hello.html', {'name': 'Test'})


def test_view(request):
    notify_customers.delay("hello")
    return render(request, 'hello.html')