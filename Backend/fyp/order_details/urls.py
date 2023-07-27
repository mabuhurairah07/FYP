from django.urls import path
from .views import ShipmentView,ShowShipmentView

urlpatterns = [
    path('shipment/', ShipmentView.as_view(), name="shipment"),
    path('show_shipment/<id>', ShowShipmentView.as_view(), name="view_shipment"),
]