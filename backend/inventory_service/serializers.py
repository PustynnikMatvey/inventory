from rest_framework import serializers
from .models import PlayerInventory

class PlayerInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerInventory
        fields = ['id', 'inventory_type', 'item_code', 'amount']

