from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path("test/", views.test_view),
    path('test_data/', views.test_data)
]
