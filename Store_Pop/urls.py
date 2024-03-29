from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from drf_spectacular.views import SpectacularAPIView , SpectacularSwaggerView

admin.site.site_header = 'StorePop Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls)),

    #! Docs
    path('api/schema/' , SpectacularAPIView.as_view() , name = 'schema') ,
    path('api/docs/' , SpectacularSwaggerView.as_view(url_name = 'schema') , name = 'swagger-ui') ,

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
