from django.urls.conf import path
from django.urls.resolvers import URLPattern

from .views import (
    data_refresh,
    ManagedEquipment,
    LatestSystemParametersView,
    FuelLevelHistoryView,
)


app_name = "monitor"


urlpatterns = [
    path("refresh/", data_refresh, name="refresh"),
    path(
        "equipment/<int:user_id>/",
        ManagedEquipment.as_view(),
        name="equipment",
    ),
    path(
        "latest-system-parameters/<int:item_id>/",
        LatestSystemParametersView.as_view(),
        name="latest_data",
    ),
    path(
        "fuel-level-history/<int:item_id>/",
        FuelLevelHistoryView.as_view(),
        name="fuel_level_history",
    ),
]
