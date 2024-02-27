from django.db import models
from django.utils import timezone


class PlayerInventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    player_id = models.BigIntegerField()
    inventory_type = models.CharField(max_length=50, default='consumable')
    item_code = models.CharField(max_length=20)
    amount = models.BigIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'player_inventory'
        unique_together = (('player_id', 'item_code'),)

class LogPlayerEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_time = models.DateTimeField(default=timezone.now)
    player_id = models.BigIntegerField(blank=False, null=False)
    event_type = models.TextField()
    event_value_type = models.TextField(default='int')
    event_value_int = models.BigIntegerField(blank=True, null=True)
    event_value_float = models.FloatField(blank=True, null=True)
    event_value_str = models.CharField(max_length=20, blank=True, null=True)
    ext_trx_id = models.CharField(max_length=40, blank=True, null=True)
    meta_data = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'log_player_event'


class PlayerInventoryTrx(models.Model):
    id = models.BigAutoField(primary_key=True)
    player_id = models.BigIntegerField()
    ext_trx_id = models.CharField(max_length=40)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'player_inventory_trx'
        unique_together = (('player_id', 'ext_trx_id'),)
