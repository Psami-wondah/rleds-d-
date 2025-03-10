from unicodedata import name
from django import urls
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from .views import ApartmentApiView
from .import views

urlpatterns = [
    path('api/v1/contact-us/', views.contact_us, name='contact_us'),
    path('api/v1/messages', views.GetMessages.as_view()),
    path('api/v1/user/<str:user_id>/messages', views.GetUserMessages.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
