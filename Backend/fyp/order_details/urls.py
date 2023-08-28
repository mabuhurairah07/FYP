from django.urls import path
from .views import *

urlpatterns = [
    path('show_shipment/<id>', ShowShipmentView.as_view(), name="view_shipment"),
    path('order/', OrderView.as_view(), name='order'),
    path('update_status/', UpdateStatusView.as_view(), name='updatestatus'),
    path('delete_order/', DeleteOrderView.as_view(), name='updatestatus'),
]