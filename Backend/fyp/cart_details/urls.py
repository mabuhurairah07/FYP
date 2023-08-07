from django.urls import path
from .views import AddToCartView,CartView

urlpatterns = [
    path('addtocart/', AddToCartView.as_view(), name="add to Cart"),
    path('cart/updated/', CartView.as_view(), name="Update_Cart"),
    path('cart/<int:id>', CartView.as_view(), name="Cart"),
    path('cart/delete/', CartView.as_view(), name="Cart-delete")
]