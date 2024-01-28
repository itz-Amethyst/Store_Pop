from django.core.mail import send_mail , mail_admins , BadHeaderError, EmailMessage
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from django.db.models import Q, F

from store.models import Product
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


def test_data(request):
    objects = Product.objects.filter(unit_price__range = (20, 30))
    object_in_range = Product.objects.filter(collection_id__range = (1,2,3))
    object_contain = Product.objects.filter(title__icontains = 'coffe')

    object_updated = Product.objects.filter(last_update__year = 2021)

    object_without_description = Product.objects.filter(description__isnull = True)

    data = serialize('json', objects)
    return JsonResponse(data = data ,safe = False)

def test_data_lookup(request):
    object = Product.objects.filter(Q(inventory__lt = 10) | Q(inventory__lt = 20))
    # Get me the products greater than 10 but not greater than 40 ~ before Q is (Not)
    object_2 = Product.objects.filter(Q(inventory__gt = 10 & ~Q(inventory__gt= 40)))
    data = serialize('json', object)
    return JsonResponse(data = data, safe = False)


def test_data_lookup_2(request):
    # Products: title == description
    object = Product.objects.filter(inventory = F('description'))

    object_2 = Product.objects.filter(pk = F('collection__id'))
    data = serialize('json' , object)
    return JsonResponse(data = data , safe = False)