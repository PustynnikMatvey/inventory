from django.db import models
from django.utils import timezone


class PlayerInventory(models.Model):
    player_id = models.IntegerField()
    item_code = models.CharField(max_length=100)
    inventory_type = models.CharField(max_length=50, default='consumable')
    amount = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)