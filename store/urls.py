from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('cart/details/', views.cartDetails, name='cartDetails'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:product_type>/', views.catalog, name='catalog'),
    path('catalog/<str:product_type>/<int:id>', views.catalog, name='catalog'),
    path('contacts/', views.contacts, name='contacts'),
]
