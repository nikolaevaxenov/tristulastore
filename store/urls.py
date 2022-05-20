from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:product_type>/', views.catalog, name='catalog'),
    path('catalog/<str:product_type>/<int:id>', views.catalog, name='catalog')
]
