from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PlayerInventory
from .serializers import PlayerInventorySerializer


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


