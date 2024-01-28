from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail , mail_admins , BadHeaderError, EmailMessage
from django.core.serializers import serialize
from django.db import transaction , connection
from django.db.models.functions import Concat
from django.forms import DecimalField
from django.http import JsonResponse
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from django.db.models import Q , F , Count , Min , Value , Func , ExpressionWrapper

from store.models import Product , OrderItem , Order
from tags.models import TaggedItem
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

def test_data_order(request):
    object = Product.objects.order_by('unit_price', '-title')

    # -unit_price, +title
    object2 = Product.objects.order_by('unit_price', '-title').reverse()

    object3 = Product.objects.order_by('title')[0]


    # Will get the latest item from descending order of title
    object4 = Product.objects.latest('title')

    data = serialize('json' , object)
    return JsonResponse(data = data , safe = False)


def test_data_limiting(request):
    # 1, 2, 3, 4
    object = Product.objects.all()[:5]


def test_data_values(request):
    # Only get this fields from Product
    object = Product.objects.values_list("title", "description", "collection__title")

    # Will get all fields except description
    object_2 = Product.objects.defer("description")

    # Distinct remove duplicates
    queryset = OrderItem.objects.values("product__id").distinct()

    object_main = Product.objects.filter(id__in = queryset).order_by('title')

    data = serialize('json', object_main)

    return JsonResponse(data = data, safe = False)

def test_data_optimizing(request):
    object = Order.objects.select_related("customer").prefetch_related('items__product').order_by('-placed_at')[:5]

    data = serialize('json' , object)

    return JsonResponse(data = data , safe = False)

def test_data_aggregate(request):
    object = Product.objects.aggregate(Count(count = 'id', min_price= Min('unit_price')))

    data = serialize('json' , object)

    return JsonResponse(data = data , safe = False)


def test_data_annotate(request):
    # To Avoid Error
    logic = ExpressionWrapper(F("unit_price" ** 2), output_field = DecimalField())

    object = Product.objects.annotate(is_new = Value("True"))

    object_2 = Product.objects.annotate(new_id = F('id') + 1)

    object_3 = Product.objects.annotate(full_name = Func(F('first_name'), Value(' ') , F('last_name'), function = 'CONCAT'))

    # Same as top but shorter
    object_4 = Product.objects.annotate(full_name = Concat('first_name', Value(' '), 'last_name'))

    object_5 = Product.objects.annotate(multipled_by_2 = logic)

    data = serialize('json' , object)

    return JsonResponse(data = data , safe = False)

def test_data_generics(request):
    # 12 => the id of table in django_content_type table
    content_type = ContentType.objects.get_for_model(Product)

    object = TaggedItem.objects.select_related("tag").filter(content_type = content_type, object_id = 1)

    # Shorter way , by implementing method in manager of the model
    TaggedItem.objects.get_tags_for(Product, 1)

@transaction.atomic
def test_save_connected_data(request):

    # .... other codes

    # Here we have a reliable query if the first goes off we might have a orderItem without order but with adding transaction we make it to work either together or none
    order = Order.objects.create(customer_id = 1)

    OrderItem.objects.create(order = order)

    #? Only applies on this part of code
    # with transaction.atomic():
    #     order = Order.objects.create(customer_id = 1)
    #     OrderItem.objects.create(order = order)

def test_data_raw_sql(request):

    Product.objects.raw("SELECT * FROM store_product")

    with connection.cursor() as cursor:
        cursor.execute('')
        cursor.callproc('get_customers', [1,2,3])