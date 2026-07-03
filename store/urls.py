from django.contrib import admin
from django.urls import path
#from .views import home,signup
from store import views
urlpatterns = [
    path('', views.home, name='homepage'),
    path("signup", views.Signup.as_view(),name='signup'),
    path("login", views.Login.as_view(),name='login'),
    path("product-detail/<int:pk>", views.productdetail,name='productdetail'),
    path("logout", views.logout,name='logout'),
    path("add_to_cart", views.add_to_cart, name='add_to_cart'),
    path("show_cart", views.show_cart, name='show_cart'),
    path("plus_cart", views.plus_cart, name='plus_cart'),
    path("minus_cart", views.minus_cart, name='minus_cart'),
    path("remove_cart", views.remove_cart, name='remove_cart'),
    path("checkout", views.checkout, name='checkout'),
    path("order/", views.order, name='order'),
    path("search/", views.search, name='search')
]