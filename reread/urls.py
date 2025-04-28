
from django.contrib import admin
from django.urls import path
from payments import views
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',include('pages.urls')),
    path('admin/',admin.site.urls),
    path('pay/', include('payments.urls')),
    path('auth/', include('user_authintication.urls')),
    path('lis/', include('listing_details.urls')),
    path('wall/', include('newsfeed.urls')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)