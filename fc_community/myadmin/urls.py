from django.urls import path
from . import views

urlpatterns = [
    path('permissions/', views.permission_list),
]
