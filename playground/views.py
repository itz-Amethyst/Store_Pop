from django.core.mail import send_mail , mail_admins , BadHeaderError, EmailMessage
from django.shortcuts import render


def say_hello(request):
    try:
        message = EmailMessage('subject', 'message', 'from@gmail.com', ['admin@gmail.com'])
        message.attach_file('uploads/store/images/productId_1/peakpx_1.jpg')
        message.send()

        # send_mail('subject', 'test message', 'info@gmail.com', '')
        mail_admins('subject', 'message', html_message = '<h2>Hi</h2>')
    except BadHeaderError:
        pass

    return render(request, 'hello.html', {'name': 'Test'})
