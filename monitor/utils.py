from decimal import Decimal
import json
import os

# from numbers import Number
from item.models import Item, ItemType
from company.models import Company, Sector
from monitor.models import Monitor
import pyrebase
from datetime import datetime
import pytz
from time import sleep


def firebase_connect():
    cred_file_path = os.path.join('..','credentials.json')
    with open(cred_file_path, "r") as file:
        credentials_dict = json.loads(file.read())
    
    firebase_config = credentials_dict["firebase_config"]

    firebase = pyrebase.initialize_app(firebase_config)

    return firebase.database()


def populate():
    # retrieve data from firebase
    db = firebase_connect()

    items = db.get()
    for keys, values in dict(items.val()).items():
        for value_key, value_val in values.items():
            for value_val_key, value_val_val in value_val.items():
                monitor_parameters = {}
                for parameter, current_val in value_val_val.items():
                    if (
                        parameter == "Hy_Oil_level"
                        and Decimal(current_val) >= 0
                    ):
                        monitor_parameters["oil_level"] = Decimal(current_val)
                    if parameter == "Ignition":
                        if current_val == "ON":
                            monitor_parameters["ignition"] = True
                        elif current_val == "OFF":
                            monitor_parameters["ignition"] = False
                    if parameter == "doors":
                        try:
                            str(current_val)
                        except:
                            pass
                        else:
                            monitor_parameters["doors"] = current_val
                    if parameter == "TimeStamp":
                        if current_val:
                            dt_object = datetime.strptime(
                                current_val, "%Y%b%d%H%M%S"
                            )
                            timezone = pytz.timezone("Africa/Lagos")
                            dt_object = timezone.localize(dt_object)
                            # print(f"datetime: {dt_object}")
                            if dt_object.year == 1970:
                                continue
                            else:
                                monitor_parameters["time_stamp"] = dt_object
                    if parameter == "company_id" and int(current_val) > 0:
                        monitor_parameters["company"] = Company(
                            id=int(current_val)
                        )
                    if parameter == "device_id" and int(current_val) > 0:
                        monitor_parameters["item"] = Item(id=int(current_val))
                    if (
                        parameter == "diesel_level"
                        and not (Decimal(current_val) > 100)
                        and Decimal(current_val) > 0
                    ):
                        monitor_parameters["fuel_level"] = Decimal(current_val)

                if "time_stamp" not in monitor_parameters.keys():
                    continue

                if Monitor.objects.filter(
                    time_stamp=monitor_parameters["time_stamp"]
                ).exists():
                    # print("event already logged")
                    continue

                if (
                    "item" in monitor_parameters.keys()
                    and "company" in monitor_parameters.keys()
                    and "fuel_level" in monitor_parameters.keys()
                ):
                    monitor_obj = Monitor.objects.get_or_create(
                        **monitor_parameters
                    )
                    try:
                        monitor_obj.save()
                    except:
                        # print("object skipped")
                        pass
                else:
                    # print("Invalid/incomplete data dropped")
                    pass


def attempt_population():
    try:
        populate()
    except:
        # print("\aProblem refreshing. Check Internet Connection!")
        pass


def run(interval=60):
    while True:
        # print("Refreshing database...")
        attempt_population()

        sleep(interval)


def clear_saved_data():
    # saved_records = list(Monitor.objects.all().prefetch_related('item').values_list('time_stamp', 'item__id').order_by('time_stamp'))

    # saved_records_list = [list(ele) for ele in saved_records]
    # saved_records_list = [[datetime.strftime(a, "%Y%b%d%H%M%S"), b] for [a, b] in saved_records_list]
    # print(saved_records_list)

    db = firebase_connect()
    db.child("device").child("001").remove()
    # db.child('device').child('001').remove()
