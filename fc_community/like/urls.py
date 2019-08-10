from django.urls import path
from . import views

urlpatterns = [
    path('like/list/', views.api_like_list),
    path('like/', views.api_like),
    path('unlike/', views.api_unlike),
]
