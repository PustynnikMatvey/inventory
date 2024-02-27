import logging

from django.shortcuts import render
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PlayerInventory, PlayerInventoryTrx, LogPlayerEvent
from .serializers import PlayerInventorySerializer

logging.basicConfig(filename='EventLogs.log', level=logging.INFO)

def get_current_amount(player_id, item_code):
    try:
        object = PlayerInventory.objects.get(player_id=player_id, item_code=item_code)
        return object.amount
    except PlayerInventory.DoesNotExist:
        return 0


class get_inventory(APIView):
    def post(self, request):
        player_id = request.data['player_id']
        try:
            # Get data from DB
            inventory = PlayerInventory.objects.filter(player_id=player_id)

            # Format the inventory data as needed
            serializer = PlayerInventorySerializer(inventory, many=True)

            # Return the inventory data as JSON response
            return Response({
                'status': 'OK',
                'data': {'player_id': player_id, 'inventory': serializer.data}
            })

        except PlayerInventory.DoesNotExist:
            return Response({'error_message': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)


class grant_item(APIView):
    def post(self, request):
        player_id = request.data['player_id']
        item_code = request.data['item_code']
        amount = request.data['amount']
        ext_trx_id = request.data['ext_trx_id']
        inventory_type = request.data['inventory_type']

        is_duplicate = False

        if player_id is None or item_code is None or amount is None:
            return Response({
                'status': 'error',
                'error_code': '400',
                'error_message': 'Missing player_id, item_code or amount',
                'context': {}
            }, status=400)

        try:
            PlayerInventoryTrx.objects.create(player_id=player_id, ext_trx_id=ext_trx_id)
        except IntegrityError:
            is_duplicate = True

        if not is_duplicate:
            obj, created = PlayerInventory.objects.update_or_create(
                player_id=player_id,
                inventory_type=inventory_type,
                item_code=item_code,
                defaults={'amount': amount + get_current_amount(player_id, item_code)}
            )
            if created:
                logging.info('A new inventory created for player_id: %s, item_code: %s, inventory_type: %s, '
                             'ext_trx_id: %s', player_id, item_code, inventory_type, ext_trx_id)
            else:
                logging.info('An existing inventory updated for player_id: %s, item_code: %s, '
                             'inventory_type: %s, ext_trx_id: %s', player_id, item_code,
                             inventory_type, ext_trx_id)

            LogPlayerEvent.objects.create(
                player_id=player_id,
                event_type='inventory_granted',
                event_value_int=amount,
                meta_data={'inventory_type': inventory_type, 'item_code': item_code},
                ext_trx_id=ext_trx_id
            )

        else:
            logging.info('Duplicate request detected when trying to grant_item player_id: %s, item_code: %s, '
                         'inventory_type: %s, ext_trx_id: %s', player_id, item_code,
                         inventory_type, ext_trx_id)

        return Response({
            'status': 'OK',
            'data': {}
        })