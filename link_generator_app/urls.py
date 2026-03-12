from django.urls import path
from .views import generate_link, protected_view

urlpatterns = [
    path('', generate_link, name='generate'),
    path('go/<str:token>/', protected_view, name='protected'),
]