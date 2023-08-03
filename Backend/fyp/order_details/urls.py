from django.urls import path
from .views import *

urlpatterns = [
    path('shipment/', ShipmentView.as_view(), name="shipment"),
    path('show_shipment/<id>', ShowShipmentView.as_view(), name="view_shipment"),
    path('order/', OrderView.as_view(), name='order'),
    path('update_order/', UpdateOrderView.as_view(), name='updateorder'),
]