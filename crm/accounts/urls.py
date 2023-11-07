from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from crm import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logoutView, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
