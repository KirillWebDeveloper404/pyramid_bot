from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from crm import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('staf/<int:id>', staf, name='staf'),
    path('user/<int:id>', user_page, name='user'),
    path('tariff/<int:id>', tariff_page, name='edit_tariff'),
    path('tariff/', tariff_page, name='add_tariff'),
    path('create_staf/', create_staf, name='create_staf'),
    path('<str:page>', main, name='main'),
]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
