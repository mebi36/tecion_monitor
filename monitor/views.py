import math
from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse

from monitor.utils import attempt_population, populate
from monitor.models import Monitor
from item.models import Item
from user.models import AppUser
from company.models import Company

from bokeh.models import (
    ColumnDataSource,
    Range1d,
    DataRange1d,
    WheelZoomTool,
    PanTool,
    ResetTool,
    BoxZoomTool,
)
from bokeh.embed import components
from bokeh.plotting import figure

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from monitor.serializers import (
    ItemSerializer,
    EquimentDataSerializer,
    EquipmentFuelLevelSerializer,
)

# Create your views here.


def datetime_val_gen(start, end, delta):
    current = start

    while current > end:
        yield current
        current -= timedelta(minutes=1)


def get_dt(interval):
    interval_delta = timedelta(minutes=interval)
    start_dt = datetime.now()
    end_dt = start_dt - interval_delta
    datetime_points = [
        dt for dt in datetime_val_gen(start_dt, end_dt, interval_delta)
    ]
    return datetime_points


def data_refresh(request):
    """a view for updating database with firebase records"""
    attempt_population()
    return HttpResponse("Refresh success!")


def dashboard(request, item_id):
    template = "monitor/dashboard.html"

    # if a normal get request is received try updating the database
    if not request.htmx:
        attempt_population()

    # preparing the data
    # check if item exists
    try:
        Item.objects.get(id=item_id)
    except:
        return HttpResponse(status=406)

    # if item does not belong to user's company return forbidden response

    range = int(request.GET.get("time_range", 60))
    dates = get_dt(range)
    dates.reverse()
    fuel_levels = []
    for date_point in dates:
        if Monitor.objects.filter(
            time_stamp__day=date_point.day,
            time_stamp__hour=date_point.hour,
            time_stamp__minute=date_point.minute,
        ).exists():
            fuel_levels.append(
                Monitor.objects.get(
                    time_stamp__day=date_point.day,
                    time_stamp__hour=date_point.hour,
                    time_stamp__minute=date_point.minute,
                ).fuel_level
            )
        else:
            fuel_levels.append(None)

    last_sys_update = Monitor.objects.aggregate(Max("time_stamp"))[
        "time_stamp__max"
    ]
    last_event_update = list(
        Monitor.objects.filter(time_stamp=last_sys_update)
        .prefetch_related("item", "company")
        .values()
    )[0]
    last_ignition_state = (
        "ON" if last_event_update["ignition"] == True else "OFF"
    )

    # chart setup
    cds = ColumnDataSource(data=dict(fuel_levels=fuel_levels, dates=dates))
    TOOLTIPS = [
        ("Update Time: ", "@dates"),
        ("Fuel Level: ", "@{fuel_levels}%"),
    ]
    fig = figure(
        x_range=DataRange1d(),
        width=700,
        height=350,
        x_axis_type="datetime",
        sizing_mode="scale_width",
        tooltips=TOOLTIPS,
        title="Fuel Level Historical Data",
        tools=[
            PanTool(dimensions="width"),
            BoxZoomTool(dimensions="width"),
            WheelZoomTool(dimensions="width"),
            ResetTool(),
        ],
    )
    fig.vbar(
        source=cds, x="dates", top="fuel_levels", width=0.8, color="#718dbf"
    )
    fig.toolbar.autohide = True
    fig.y_range = Range1d(0, 100)
    fig.xaxis.major_label_orientation = math.pi / 2
    fig.title.align = "center"
    fig.title.text_font_size = "1.5em"
    script, div = components(fig)

    # preparing to render
    context = {
        "script": script,
        "div": div,
        "last_sys_update": last_sys_update,
        "last_fuel_level": last_event_update["fuel_level"],
        "last_oil_level": last_event_update["oil_level"],
        "last_ignition_state": last_ignition_state,
    }

    if request.htmx:
        return render(request, "monitor/partials/dashboard.html", context)
    return render(request, template, context)


# @login_required
# def managed_equipment(request):
#     template = 'monitor/managed_equipment.html'
#     all_user_equipment = Item.objects.all().filter(company=request.user.company)
#     if len(all_user_equipment) > 0:
#         context = {'managed_equipment': all_user_equipment}

#     return render(request, template, context)


# =====================================================


class ManagedEquipment(APIView):
    def get(self, request, user_id, format=None):
        equipment_list = Item.objects.all().filter(
            company=AppUser.objects.get(id=user_id).company
        )
        serializer = ItemSerializer(equipment_list, many=True)
        return Response(serializer.data)


class LatestSystemParametersView(APIView):
    """a CBV for handling the rendering of data of a specific equipment"""

    def get(self, request, item_id, format=None):
        equipment_data = (
            Monitor.objects.filter(item=Item(id=item_id))
            .order_by("-time_stamp")
            .first()
        )
        # import random
        # equipment_data = {'fuel_level': random.randint(1, 100)}
        serializer = EquimentDataSerializer(equipment_data)
        return Response(serializer.data)


class FuelLevelHistoryView(APIView):
    """a CBV for handling the rendering of a particular equipment's fuel
    leve history"""

    def get(self, request, item_id, format=None):
        fuel_history = Monitor.objects.filter(item=Item(id=item_id)).order_by(
            "time_stamp"
        )
        serializer = EquipmentFuelLevelSerializer(fuel_history, many=True)

        return Response(serializer.data)
