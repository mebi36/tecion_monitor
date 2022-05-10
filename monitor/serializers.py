from rest_framework import serializers
from monitor.models import Monitor
from item.models import Item, ItemType

# class MonitorSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ["id", "name"]


class ItemSerializer(serializers.ModelSerializer):
    type = ItemTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = ("id", "type", "description", "get_latest_data_url")


# class ManagedEquipmentSerializer(serializers.ModelSerializer):


class EquimentDataSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, read_only=True)

    class Meta:
        model = Monitor
        fields = ["item", "oil_level", "ignition", "fuel_level", "time_stamp"]


class EquipmentFuelLevelSerializer(serializers.ModelSerializer):
    # item = ItemSerializer(many=False, read_only=True)

    class Meta:
        model = Monitor
        fields = ["time_stamp", "fuel_level"]
